\version "2.24.0"

% \transpose FROM TO { music } must emit the SOUNDING pitches: c e g c
% transposed c->d sounds d fs a d, and a \key inside the block transposes
% with it (c major -> d major). Music after the block is back at written
% pitch. Without a handler the parser descended into the block and emitted
% the written pitches - valid XML with wrong notes.

\score {
  {
    \time 4/4
    \transpose c d { \key c \major c'4 e'4 g'4 c''4 }
    c'4 e'4 g'4 c''4
  }
  \layout {}
}
