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


def test_tremolo_repeat():
    compare_output('tremolo_repeat')


def test_variable_dotted():
    compare_output('variable_dotted')


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
