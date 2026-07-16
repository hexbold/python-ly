\version "2.24.0"

% A grace pair inside a tuplet: grace notes have no <duration> element, so
% the tuplet duration rewrite must not touch the PREVIOUS note through the
% remembered duration node (it corrupted it to a fraction like 8/3), and the
% intra-note nested-tuplet factor must not leak across notes.

\score {
  {
    \time 4/4
    \tuplet 3/2 { c'8 \grace { d'16 e'16 } f'8 g'8 } a'4 b'4 c''4
  }
  \layout {}
}
