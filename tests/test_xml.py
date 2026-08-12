"""Tests for XML output."""
import datetime
import difflib
import glob
import ly.musicxml
from lxml import etree
import os
import os.path
import io
import pytest
import re
import sys


def test_glissando():
    compare_output('glissando')


def test_tie():
    compare_output('tie')


def test_merge_voice():
    compare_output('merge_voice')


def test_variable():
    compare_output('variable')


def test_dynamics():
    compare_output('dynamics')


def test_tuplet():
    compare_output('tuplet')


def test_bar_duration_grace_tuplet():
    compare_output('bar_duration_grace_tuplet')


def test_accidental_display():
    compare_output('accidental_display')


def test_accidental_rule():
    compare_output('accidental_rule')


def test_beams():
    compare_output('beams')


def test_navigation():
    compare_output('navigation')


def test_lyrics_sibling():
    # A \lyricsto Lyrics context that is a SIBLING of the staff (the idiomatic
    # song layout) must still reach its voice, whose section is already merged
    # into the part when the lyrics arrive.
    compare_output('lyrics_sibling')


def test_lyrics_verses():
    # Two \lyricsto contexts onto one voice are verses 1 and 2; their lyrics
    # must be numbered so consumers can stack them.
    compare_output('lyrics_verses')


def test_pedal():
    # \sustainOn/\sustainOff become <pedal type="start"/"stop"> directions.
    compare_output('pedal')


def test_markup_note():
    # Note-attached markup flattens to its plaintext as a <words> direction,
    # like a plain quoted string does.
    compare_output('markup_note')


def test_transpose():
    # \transpose emits the SOUNDING pitches (and transposes an inner \key);
    # music after the block returns to written pitch.
    compare_output('transpose')


def test_chord_repetition():
    # q with a new duration must feed the divisions computation: the eighth
    # copies used to get XSD-invalid <duration>0</duration>.
    compare_output('chord_repetition')


def test_spacer_rests():
    # s and \skip become invisible rests (print-object="no"), and a measure
    # ending in a spacer gets no spurious <backup>.
    compare_output('spacer_rests')


def test_tuplet_grace():
    # A grace inside a tuplet must not corrupt the previous note's <duration>
    # through the remembered duration node, nor leak the tuplet factor.
    compare_output('tuplet_grace')


def test_lyrics_melisma():
    # \lyricsto skips slur and tie continuations (LilyPond's melisma rule),
    # not only notes behind a __ extender.
    compare_output('lyrics_melisma')


def test_header_tagline():
    # Empty header values (tagline = ##f) must be skipped, and identification
    # children must keep call order (creator before rights, before encoding).
    compare_output('header_tagline')


def test_header_credits():
    # Header fields must also emit <credit> blocks — page-header renderers
    # (Verovio, MuseScore) draw only the title without them. "poet" maps to
    # the credit vocabulary's lyricist.
    compare_output('header_credits')


def test_tremolo_repeat():
    compare_output('tremolo_repeat')


def test_variable_dotted():
    compare_output('variable_dotted')


def test_variable_simultaneous():
    # A variable whose WHOLE BODY is << { } \\ { } >> (no outer braces): the
    # substituted container never got its End event (iter_score tested the
    # UserCommand, not the substituted node), so the block's first voice was
    # dropped silently and every note after it shifted to voice 2.
    compare_output('variable_simultaneous')


def test_quoted_vars():
    # Quoted assignments ("mel.1" = ...) referenced as \"mel.1" used to be
    # dropped silently (exit 0, zero notes): the lexer had no rule for a
    # backslash before a quoted string, and a quoted name was never read as
    # an Assignment.
    compare_output('quoted_vars')


def test_tempo_before_music():
    compare_output('tempo_before_music')


def test_staffgroup_nested():
    compare_output('staffgroup_nested')


def test_final_barline():
    compare_output('final_barline')


def test_final_barline_single():
    compare_output('final_barline_single')


def test_pianostaff_voices():
    compare_output('pianostaff_voices')


def test_marcato():
    compare_output('marcato')


def test_tempo_range():
    compare_output('tempo_range')


def test_arpeggio():
    compare_output('arpeggio')


def test_grace_slash():
    compare_output('grace_slash')


def test_text_script():
    compare_output('text_script')


def test_volta_alternative():
    compare_output('volta_alternative')

def test_merge_voice_slurs():
    compare_output('merge_voice_slurs')

def test_break():
    compare_output('break')


def test_mark():
    compare_output('mark')


def test_partial():
    compare_output('partial')


def test_partial_time():
    compare_output('partial_time')


def test_full_bar():
    compare_output('full_bar_rest')


def test_multibar_rest():
    compare_output('multibar_rest')


def test_stem_direction():
    compare_output('stem')


def test_church():
    compare_output('church_modes')


def test_markup():
    # was xfail for years: note-attached markup words used to land in the
    # wrong measure (or vanish, for quoted/formatted markup)
    compare_output('markup')


def test_breathe():
    compare_output('breathe')


def test_no_barcheck():
    compare_output('no_barcheck')


def test_chord_duration():
    compare_output('chord_duration')


def test_staff_attr_before_voice():
    # Attributes written in a staff block BEFORE its \new Voice (e.g.
    # \new Staff { \tempo 4 = 72 \new Voice = "mel" \melody }) must fold into
    # the first measure — they used to become a phantom empty first measure,
    # shifting the voice one measure against every other part.
    compare_output('staff_attr_before_voice')


def test_time_cut():
    compare_output('time_cut')


def ly_to_xml(filename):
    """Read Lilypond file and return XML string."""
    writer = ly.musicxml.writer()
    with open(filename, 'r') as lyfile:
        writer.parse_text(lyfile.read())
    xml = writer.musicxml()
    sio = io.BytesIO()
    xml.write(sio, "utf-8")
    return sio.getvalue().decode("utf-8")

encoding_date_element_re = re.compile(r'(?<=<encoding-date>)\d{4}-\d{2}-\d{2}(?=</encoding-date>)')

def read_expected_xml(filename):
    """Return string with expected XML from file."""
    with open(filename, 'r') as xmlfile:
        output = xmlfile.read()
    # Replace date in XML file with today's date
    output = encoding_date_element_re.sub(str(datetime.date.today()), output)
    return output


def compare_output(filename):
    """Compare XML output with expected output."""
    filebase = os.path.join(os.path.dirname(__file__), 'test_xml_files',
                            filename)

    output = ly_to_xml(filebase + '.ly')
    expected_output = read_expected_xml(filebase + '.xml')

    assert_multi_line_equal(expected_output, output)
    validate_xml(output)


def validate_xml(xml):
    """Validate XML against XSD file."""
    xsdname = os.path.join(os.path.dirname(__file__), 'musicxml.xsd')
    xsdfile = open(xsdname, 'r')
    xmlschema_doc = etree.parse(xsdfile)
    xsdfile.close()
    xmlschema = etree.XMLSchema(xmlschema_doc)
    parser = etree.XMLParser(schema=xmlschema)
    xml_bytes = xml.encode('utf-8')
    # Raises Exception if not valid:
    etree.fromstring(xml_bytes, parser)


def assert_multi_line_equal(first, second, msg=None):
    """Assert that two multi-line strings are equal.

    If they aren't, show a nice diff.
    """
    assert isinstance(first, str), 'First argument is not a string'
    assert isinstance(second, str), 'Second argument is not a string'

    if first != second:
        message = ''.join(difflib.ndiff(first.splitlines(True),
                                        second.splitlines(True)))
        if msg:
            message += " : " + msg
        assert False, "Multi-line strings are unequal:\n" + message


def regenerate_xml():
    """Regenerate the XML files"""
    extension_re = re.compile(r'\.ly$')
    for ly_path in glob.glob(os.path.join(os.path.dirname(__file__), 'test_xml_files/*.ly')):
        xml_path = extension_re.sub('.xml', ly_path)
        xml = ly_to_xml(ly_path)
        with open(xml_path, 'w') as fw:
            fw.write(xml)


# Run
#   $ test_xml.py regenerate
# to generate the expected XML files anew with current python-ly
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'regenerate':
        regenerate_xml()


def test_srcmap():
    # The opt-in source map (ly/musicxml/srcmap.py): with srcmap=True the writer
    # records, for every emitted note/rest/directive, the span in the parsed text
    # it came from — without changing the XML output at all.
    source = ('\\version "2.18.0"\n'
              '\\header { title = "Probe" }\n'
              'up = { \\clef treble \\key c \\major \\time 4/4 \\tempo 4 = 96\n'
              '  c\'4\\p-. d\'8 ees\'8 e\'4 <g\' b\'>4~ | <g\' b\'>4 q4 r4 gis\'4 }\n'
              '\\score { \\new Staff \\up \\midi {} }\n')

    def to_string(xml):
        sio = io.BytesIO()
        xml.write(sio, "utf-8")
        return sio.getvalue().decode("utf-8")

    plain = ly.musicxml.writer()
    plain.parse_text(source)
    baseline = to_string(plain.musicxml())

    e = ly.musicxml.writer(srcmap=True)
    e.parse_text(source)
    output = to_string(e.musicxml())
    assert output == baseline          # collection never changes the XML
    m = e.srcmap()

    assert m["v"] == 1 and m["positions_valid"] is True
    assert m["parts"] == [{"name": "", "staves": 1}]
    # every <note> element has exactly one event, in emission order
    assert len(m["events"]) == output.count("<note")

    def sliced(span):
        return source[span[0]:span[1]]

    spans = [sliced(e["span"]) for e in m["events"] if "span" in e]
    # q-copies are materialized without source tokens and carry no span
    assert spans == ["c'", "d'", "ees'", "e'", "g'", "b'",
                     "g'", "b'", "r", "gis'"]
    # chord members share the event ordinal, counting `member` up
    chord = [e for e in m["events"] if e["measure"] == 1 and e["idx"] == 4]
    assert [(e["member"], sliced(e["span"])) for e in chord] == [(0, "g'"), (1, "b'")]
    # every event carries its notated length in whole notes (dur), dots folded in
    assert m["events"][0]["dur"] == [1, 4]
    assert m["events"][1]["dur"] == [1, 8]
    # note-attached tokens (dynamics, articulations, ties) carry their own spans
    first = m["events"][0]
    attach = {a[0]: sliced((a[2], a[3])) for a in first["attach"]}
    assert attach["dyn"] == "\\p" and attach["artic"] == "."
    # standalone directives and header fields map to their full source text
    objs = {o["kind"]: sliced(o["span"]) for o in m["objects"]}
    assert objs["key"] == "\\key c \\major"
    assert objs["time"] == "\\time 4/4"
    assert objs["clef"] == "\\clef treble"
    assert objs["tempo"] == "\\tempo 4 = 96"
    assert sliced(m["header"]["title"]) == '"Probe"'


def test_srcmap_mrest_run_copies_keep_the_staff():
    # R1*n materializes n-1 copy bars; the copies carry no span but MUST keep the
    # owner's staff — they used to default to staff 1, splitting a lower-staff run
    # across staves in the map.
    source = ('\\version "2.18.0"\n'
              'up = { \\clef treble \\time 4/4 c\'\'1 | d\'\'1 | e\'\'1 | }\n'
              'lo = { \\clef bass \\time 4/4 c1 | R1*2 | }\n'
              '\\score { \\new PianoStaff << \\new Staff \\up \\new Staff \\lo >> \\midi {} }\n')
    e = ly.musicxml.writer(srcmap=True)
    e.parse_text(source)
    e.musicxml()
    m = e.srcmap()
    mrests = [ev for ev in m["events"] if ev["kind"] == "mrest"]
    assert [ev.get("staff") for ev in mrests] == [2, 2]
    assert mrests[0].get("span") and not mrests[1].get("span")


def test_srcmap_relative_positions_flagged_invalid():
    # \relative input is converted to absolute pitches before parsing, so the
    # spans index the CONVERTED text — the map must say its positions are not
    # valid for the caller's original text.
    source = ('\\version "2.18.0"\n'
              "\\score { \\relative c'' { c4 d e f } \\midi {} }\n")
    e = ly.musicxml.writer(srcmap=True)
    e.parse_text(source)
    e.musicxml()
    assert e.srcmap()["positions_valid"] is False


def test_direction_staff_in_multistaff_part():
    # Issue 46: a note-attached <direction> (dynamics, wedge, pedal) must carry its
    # note's <staff> in a multi-staff part — without it MusicXML defaults the direction
    # to staff 1, so every left-hand piano dynamic renders under the RIGHT hand's staff.
    # Single-staff parts keep emitting no <staff> (output unchanged).
    source = ('\\version "2.18.0"\n'
              "rh = { e''2\\mf d''2\\< c''2 b'2\\! }\n"
              "lh = { \\clef bass c2\\p e2 g2\\sustainOn c'2\\sustainOff }\n"
              "\\score { \\new PianoStaff << \\new Staff \\rh \\new Staff \\lh >> \\midi {} }\n")
    e = ly.musicxml.writer()
    e.parse_text(source)
    xml = e.musicxml()
    sio = io.BytesIO()
    xml.write(sio, "utf-8")
    output = sio.getvalue().decode("utf-8")

    import xml.etree.ElementTree as ET
    root = ET.fromstring(output)
    staffed = [d.findtext("staff") for d in root.iter("direction")]
    # rh: mf + wedge start + wedge stop on staff 1; lh: p + two pedals on staff 2
    assert staffed.count("1") == 3
    assert staffed.count("2") == 3
    assert None not in staffed

    single = ('\\version "2.18.0"\n'
              "\\score { { c'2\\p d'2 } \\midi {} }\n")
    e = ly.musicxml.writer()
    e.parse_text(single)
    xml = e.musicxml()
    sio = io.BytesIO()
    xml.write(sio, "utf-8")
    root = ET.fromstring(sio.getvalue())
    assert [d.findtext("staff") for d in root.iter("direction")] == [None]


def test_after_grace_with_articulation():
    r"""\afterGrace main-note-with-postfix { graces }: the postfix (\trill)
    must not be counted as the second music argument — the grace group used
    to escape the wrapper as REAL timed notes, shifting the voice by the
    group's duration (audibly desyncing the hands after every trill)."""
    source = ('\\version "2.24.0"\n'
              '\\language "english"\n'
              '\\score { \\new Staff { \\time 12/8 '
              "\\afterGrace fs''2.\\trill { e''16[ fs''16] } c''2. } \\layout {} }\n")
    w = ly.musicxml.writer()
    w.parse_text(source)
    xml = w.musicxml()
    sio = io.BytesIO()
    xml.write(sio, "utf-8")
    output = sio.getvalue().decode("utf-8")

    import xml.etree.ElementTree as ET
    root = ET.fromstring(output)
    notes = list(root.iter("note"))
    graces = [n for n in notes if n.find("grace") is not None]
    timed = [n for n in notes if n.find("grace") is None]
    # the two termination notes are grace notes without duration
    assert len(graces) == 2
    assert all(n.find("duration") is None for n in graces)
    # the timed notes fill the 12/8 measure exactly: 2. + 4. and nothing more
    divisions = int(root.find(".//divisions").text)
    assert sum(int(n.findtext("duration")) for n in timed) == divisions * 6
    # the trill survives on the main note
    assert len(root.findall(".//trill-mark")) == 1
    validate_xml(output)


def test_tuplet_ending_in_rest():
    r"""A tuplet whose last event is a rest or spacer: the stop marker lands
    on the rest (used to raise IndexError and kill the export), and rests
    inside tuplets carry <time-modification> like notes."""
    compare_output('tuplet_rest')


def test_slur_stop_on_rest():
    r"""LilyPond allows c( d r) — MusicXML slurs attach to notes only, so
    the stop moves to the last sounding note (used to crash: BarRest has no
    set_slur)."""
    compare_output('slur_on_rest')


def test_tie_into_chord():
    r"""c'~ <c' e'> ties ONLY the matching pitch: the other chord member
    used to inherit a spurious tie stop via the shared tie list. Chord-to-
    chord ties still tie every member."""
    compare_output('tie_into_chord')


def test_inline_polyphony_bar_accounting():
    r"""<< .. \\ .. >> inside a voice: bar_dura is saved per block and each
    branch restarts at the block's start, so music after the block continues
    its bar and later bars close on time. Also covers nesting, a shorter
    first branch (list_full propagation through merge_voice) and the
    PianoStaff staff merge that used to truncate to the shortest staff.
    \voiceX inside a branch no longer remaps the MusicXML voice number
    (double-booked voices made MuseScore reject the file)."""
    compare_output('polyphony_inline')


def test_header_opus_is_work_number():
    r"""\header opus lands in <work><work-number>, not in <identification>
    (schema-invalid there — MuseScore refused every file carrying it)."""
    compare_output('header_opus')


def test_after_command_duration_not_a_note():
    r"""\after DUR EVENT MUSIC: the bare duration argument must not become
    a repeated-pitch note (phantom time shifted the whole voice)."""
    compare_output('after_command')


def test_duration_multiplier_divisions():
    r"""Duration multipliers like *8/9 pick the minimal divisions growth:
    the old factor ignored scaling, so every scaled note re-multiplied
    divisions — 70-digit divisions that no reader could parse."""
    compare_output('duration_multipliers')


def test_pitched_rest_closing_its_bar():
    r"""The \rest command arrives after its note; when that note just filled
    the measure, self.bar has moved on — popping there destroyed the fresh
    bar's attributes and left the note a sounding pitch."""
    compare_output('rest_pitched_barend')


def test_partial_midpiece_between_repeats():
    r"""An upbeat opening the SECOND \repeat volta (first block ends on the
    complementary short measure): \partial must close the open short bar,
    or both merge into one overfull measure and every later barline
    shifts."""
    compare_output('partial_midpiece')


def test_tuplet_span_duration_not_inherited():
    r"""\tuplet 3/2 8 { ... }: the 8 is the bracket span unit — it must not
    become the inherited duration of the notes inside (they came out double
    length, overfilling the measure)."""
    compare_output('tuplet_span')


def test_polyphony_straddling_barline():
    r"""A << .. \\ .. >> block crossing a barline leaves a PARTIAL backup in
    the second measure; the backup for the next merged voice must still
    rewind the full measure (summing since the last backup overflowed the
    measure and time-shifted the rest of the piece). The block's branches
    also skip voice numbers claimed by explicit \voiceX commands anywhere
    in the source, so a branch never double-books a sibling voice (readers
    merge the two streams destructively or reject the file)."""
    compare_output('polyphony_straddling_barline')


def test_simultan_meter_scope():
    r"""A \time change inside one voice of a << .. >> group: parallel
    voices all start at the meter the group opened with, not at whatever
    the previously parsed sibling ended in (voice 2's bars closed on the
    wrong sums from its first bar, mincing the whole part)."""
    compare_output('simultan_meter_scope')
