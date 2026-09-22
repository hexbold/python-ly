"""Regression coverage for explicit Voice groups inside sequential music.

The converter must preserve note positions, distinct parallel
streams, and source provenance when returning to the enclosing voice.
"""

from fractions import Fraction
import xml.etree.ElementTree as ET

import pytest

import io
import ly.musicxml


def convert(music, *, piano=False, extra="", definitions=""):
    staff = r"\new Staff { \clef treble \time 4/4 " + music + " }"
    if piano:
        staff = (r"\new PianoStaff << " + staff
                 + r" \new Staff { \clef bass c1 c1 c1 } >>")
    source = (r'\version "2.24.0" \language "english" '
              + definitions + r"\score { << " + staff + extra + r" >> \layout {} }")
    writer = ly.musicxml.writer(srcmap=True)
    writer.parse_text(source)
    output = io.BytesIO()
    writer.musicxml().write(output, "utf-8")
    xml, srcmap = output.getvalue(), writer.srcmap()
    root = ET.fromstring(xml)
    # Every materialized note retains its original pitch token, including
    # the formerly lost continuation after the simultaneous group.
    notes = root.findall(".//note")
    assert srcmap["positions_valid"] is True
    assert len(srcmap["events"]) == len(notes)
    for note, event in zip(notes, srcmap["events"]):
        if note.find("pitch") is None:
            assert note.get("print-object") == "no"  # implicit branch padding
            continue
        span = event["span"]
        octave = int(note.findtext("pitch/octave")) - 3
        token = note.findtext("pitch/step").lower() + (
            "'" * octave if octave >= 0 else "," * -octave)
        assert source[span[0]:span[1]] == token
    return root


def events(root, staff="1"):
    """Read exact measure-local times from MusicXML's backup/forward stream."""
    result = []
    divisions = 1
    for measure in root.findall("part/measure"):
        cursor = Fraction(0)
        previous = cursor
        for node in measure:
            if node.tag == "attributes":
                divisions = int(node.findtext("divisions", str(divisions)))
            duration = Fraction(int(node.findtext("duration", "0")), divisions)
            if node.tag == "backup":
                cursor -= duration
                assert cursor >= 0
            elif node.tag == "forward":
                cursor += duration
            elif node.tag == "note":
                onset = previous if node.find("chord") is not None else cursor
                if node.findtext("staff", "1") == staff and node.find("pitch") is not None:
                    result.append((int(measure.get("number")),
                                   node.findtext("pitch/step")
                                   + node.findtext("pitch/octave"),
                                   onset, duration, node.findtext("voice", "1")))
                if node.find("chord") is None:
                    previous = cursor
                    cursor += duration
    return result


@pytest.mark.parametrize("piano", [False, True])
def test_inline_voice_continuation_keeps_measures_and_source_map(piano):
    root = convert(r"c'1 << \new Voice { e'1 } \new Voice { g'1 } >> c'1",
                   piano=piano)
    assert events(root) == [
        (1, "C4", 0, 4, "1"), (2, "E4", 0, 4, "1"),
        (2, "G4", 0, 4, "2"), (3, "C4", 0, 4, "1"),
    ]
    assert root.findtext(".//clef/sign") == "G"
    assert root.findtext(".//time/beats") == "4"
    if piano:
        assert events(root, "2") == [(m, "C3", 0, 4, "5") for m in (1, 2, 3)]


def test_midbar_voice_group_crosses_barline_and_resumes_at_correct_beat():
    root = convert(r"c'2. << \new Voice { e'4 f'4 } "
                   r"\new Voice { g'4 a'4 } >> b'2. c''1")
    assert events(root) == [
        (1, "C4", 0, 3, "1"), (1, "E4", 3, 1, "1"),
        (1, "G4", 3, 1, "2"), (2, "F4", 0, 1, "1"),
        (2, "A4", 0, 1, "2"), (2, "B4", 1, 3, "1"),
        (3, "C5", 0, 4, "1"),
    ]


@pytest.mark.parametrize("branches", [
    r"\new Voice { e'2 } \new Voice { g'4 }",
    r"\new Voice { e'4 } \new Voice { g'2 }",
])
def test_continuation_uses_longest_branch_not_last_parsed_branch(branches):
    root = convert("c'2 << " + branches + " >> c''4 d''4 e''4 f''4 g''1")
    assert [event for event in events(root) if event[1].endswith("5")] == [
        (2, "C5", 0, 1, "1"), (2, "D5", 1, 1, "1"),
        (2, "E5", 2, 1, "1"), (2, "F5", 3, 1, "1"),
        (3, "G5", 0, 4, "1"),
    ]


def test_shorter_last_branch_pads_to_continuation_beat_inside_measure():
    root = convert(r"c'4 << \new Voice { e'2 } \new Voice { g'4 } >> c''4 d''1")
    assert events(root)[-2:] == [(1, "C5", 3, 1, "1"), (2, "D5", 0, 4, "1")]


def test_shorter_last_branch_pads_across_a_barline():
    root = convert(r"c'2. << \new Voice { e'4 f'4 } \new Voice { g'8 } >> a'2. b'1")
    assert events(root)[-2:] == [(2, "A4", 1, 3, "1"), (3, "B4", 0, 4, "1")]


def test_shorter_branch_padding_obeys_enclosing_tuplet():
    root = convert(r"\tuplet 3/2 { c'4 << \new Voice { e'4 } "
                   r"\new Voice { g'8 } >> a'4 } b'2 c''1")
    assert events(root)[-3:] == [
        (1, "A4", Fraction(4, 3), Fraction(2, 3), "1"),
        (1, "B4", 2, 2, "1"), (2, "C5", 0, 4, "1"),
    ]


@pytest.mark.parametrize("branches", [
    r"{ e'2 } \new Voice { g'4 }",
    r"\new Voice { e'2 } { g'4 }",
])
def test_mixed_braced_and_explicit_voice_branches_share_the_start(branches):
    root = convert("c'4 << " + branches + " >> c''4 d''1")
    assert events(root) == [
        (1, "C4", 0, 1, "1"), (1, "E4", 1, 2, "1"),
        (1, "G4", 1, 1, "2"), (1, "C5", 3, 1, "1"),
        (2, "D5", 0, 4, "1"),
    ]


def test_repeated_variable_branches_mix_with_explicit_voice():
    root = convert(r"c'4 << \branch \new Voice { g'4 } \branch >> c''4 d''1",
                   definitions=r"branch = { e'2 } ")
    assert events(root) == [
        (1, "C4", 0, 1, "1"), (1, "E4", 1, 2, "1"),
        (1, "G4", 1, 1, "2"), (1, "E4", 1, 2, "3"),
        (1, "C5", 3, 1, "1"), (2, "D5", 0, 4, "1"),
    ]


@pytest.mark.parametrize("inner", [
    r"<< { e'4 } \\ { g'4 } >>",
    r"<< \new Voice { e'4 } \new Voice { g'4 } >>",
])
def test_nested_voice_branches_do_not_reuse_a_simultaneous_voice_number(inner):
    root = convert(r"c'2 << \new Voice { " + inner
                   + r" f'4 } \new Voice { a'2 } >> c''1")
    assert events(root) == [
        (1, "C4", 0, 2, "1"), (1, "E4", 2, 1, "1"),
        (1, "G4", 2, 1, "2"), (1, "F4", 3, 1, "1"),
        (1, "A4", 2, 2, "3"), (2, "C5", 0, 4, "1"),
    ]


def test_named_inline_voices_keep_their_own_lyrics_after_merging():
    root = convert(
        r'''c'1 << \new Voice = "melody" { e'2 f'2 }
        \new Voice = "counter" { g'2 a'2 } >> c''1''',
        extra=r''' \new Lyrics \lyricsto "melody" { first voice }
                   \new Lyrics \lyricsto "counter" { other line }''')
    assert [(note.findtext("pitch/step"), note.findtext("lyric/text"))
            for note in root.findall(".//note")] == [
        ("C", None), ("E", "first"), ("F", "voice"),
        ("G", "other"), ("A", "line"), ("C", None),
    ]
