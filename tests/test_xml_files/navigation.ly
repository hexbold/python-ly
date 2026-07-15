\version "2.24.0"

% Segno and coda are navigation elements in MusicXML, not rehearsal marks: a reader
% follows them for D.S. and D.C. jumps, so rendering them as a <rehearsal> letter loses
% the meaning. Both spellings must reach the same elements: the classic
% \mark \markup { \musicglyph "scripts.segno" } and the 2.24 \segnoMark / \codaMark.
% A plain \mark \default must still be a rehearsal letter, and the segno must not eat one.

\score {
  \new Staff {
    \time 4/4
    c'1 |
    \mark \markup { \musicglyph "scripts.segno" }
    d'1 |
    \mark \markup { \musicglyph "scripts.coda" }
    e'1 |
    \segnoMark \default
    f'1 |
    \codaMark \default
    g'1 |
    \mark \default
    a'1 |
  }
  \layout { }
}
