\version "2.24.0"

% \bar "|." at the end of the piece: bars close eagerly when full, so at
% \bar time the current bar is already a fresh empty one. The barline
% landed there and another bar was opened — producing a phantom empty
% final measure (which strict importers like MuseScore 4 reject) with
% the barline rendered in the wrong measure.

rh = { \clef treble \time 4/4 c'4 d' e' f' | g'1 \bar "|." }
lh = { \clef bass \time 4/4 c4 d e f | g1 }

\score {
  \new PianoStaff <<
    \new Staff \rh
    \new Staff \lh
  >>
  \layout { }
}
