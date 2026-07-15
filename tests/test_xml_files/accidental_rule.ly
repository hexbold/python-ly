\version "2.24.0"

% Where a printed accidental goes. <accidental> is the sign on the page and <alter> is
% the pitch; they are independent, and consumers do not re-derive the sign from the pitch
% (Verovio draws none without it), so the exporter has to work out where one is notated.
% The rule, and what LilyPond engraves: a sign is printed when a note's alteration differs
% from the one in force for its staff, step and octave, which is the key signature until an
% earlier note in the same bar overrides it.

\score {
  \new Staff {
    \key c \major \time 4/4
    cis'4 cis'4 c'4 e'4 |
    cis'4 cis''4 r2 |
    cis'1~ |
    cis'4 cis'4 r2 |
  }
  \layout { }
}
