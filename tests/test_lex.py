"""Tests for the lexers."""
import ly.document
import ly.lex._token
import ly.lex.html
import ly.lex.lilypond


DIGIT_TOKENS = (ly.lex._token.Numeric,
                ly.lex.lilypond.Fingering,
                ly.lex.lilypond.StringNumber,
                ly.lex.lilypond.ChordStepNumber,
                ly.lex.lilypond.FigureStep,
                ly.lex.lilypond.TempoSeparator,
                ly.lex.lilypond.Scaling)

TO_FULLWIDTH = str.maketrans('0123456789', '０１２３４５６７８９')

SOURCES = [
    '#(display 42)',
    '#(x 1/2)',
    '#(x 1.5)',
    '\\tempo 4 = 60 - 80',
    '\\time 3/4',
    'c4',
    'c-4',
    '\\override NoteHead.font-size = 2',
    '\\chords { c1:5 }',
    '\\figures { <1> }',
    '\\score { { c1*2 } }',
    '\\score { \\new TabStaff { c4\\4 } }',
]


def digit_tokens(text, mode=None):
    """Return the text of every token the lexer only reads as such because of
    the digits in it."""
    doc = ly.document.Document(text, mode)
    return [str(t) for block in doc
            for t in doc.tokens(block) if isinstance(t, DIGIT_TOKENS)]


def test_ascii_digits_are_read():
    for source in SOURCES:
        assert digit_tokens(source), source


def test_fullwidth_digits_are_not_read():
    for source in SOURCES:
        fullwidth = source.translate(TO_FULLWIDTH)
        assert digit_tokens(fullwidth) == [], fullwidth


def entity_refs(text):
    doc = ly.document.Document(text, 'html')
    return [str(t) for block in doc
            for t in doc.tokens(block) if isinstance(t, ly.lex.html.EntityRef)]


def test_only_ascii_digits_form_a_numeric_entity():
    assert entity_refs('&#65;') == ['&#65;']
    assert entity_refs('&#65;'.translate(TO_FULLWIDTH)) == []
