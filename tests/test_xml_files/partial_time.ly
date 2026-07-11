\version "2.24.0"

% \partial after \time: the current bar already exists (created for the
% time signature), so the pickup mark must go on THAT bar, and the
% duration bookkeeping must close it after exactly the pickup length —
% otherwise the pickup bar swallows notes of the next measure and every
% later barline shifts.

melody = {
  \clef treble \time 3/4
  \partial 4 g'4 |
  c''4 d''4 e''4 |
  c''2.
}

\score {
  \new Staff \melody
  \layout { }
}
