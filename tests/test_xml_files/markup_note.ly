\version "2.24.0"

% A note-attached markup (c'4^\markup { \italic "dolce" }) flattens to its
% plaintext as a <words> direction at the note's position, the same way a
% plain quoted string (^"espr.") does. Formatting is dropped, text kept.

\score {
  { \time 4/4 c'4^"espr." d'4 e'4^\markup { \italic "dolce" } f'4 }
  \layout {}
}
