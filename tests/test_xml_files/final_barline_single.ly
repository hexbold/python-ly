\version "2.24.0"

% A final \bar "|." on a SINGLE staff. The barline lives on the part's
% last bar, but merging the global section back into the lone part popped
% it (the global section is skip-only, so its copy was never re-added).

melody = { \clef treble \time 4/4 c'4 d' e' f' | g'1 \bar "|." }

\score {
  \new Staff \melody
  \layout { }
}
