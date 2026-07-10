\version "2.24.0"

% Dotted variable names (LilyPond 2.20+): vc.1 = { ... } referenced as
% \vc.1. Unfixed code built no Assignment for the dotted name and misread
% the reference as \vc plus a standalone duration, so the notes vanished
% from the export entirely.

vc.1 = { c'4 d' e' f' }
vc.2 = { g'1 }
cello = { \clef bass \time 4/4 \vc.1 | \vc.2 }

\score {
  \new Staff \cello
  \layout { }
}
