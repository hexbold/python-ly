\version "2.24.0"

% q repeats the previous chord. With a NEW duration (q8 after a quarter
% chord) the copies must feed the divisions computation like any note:
% divisions used to stay 1 and the eighth copies got <duration>0</duration>,
% which is XSD-invalid (minExclusive).

\score {
  { \time 4/4 <c' e'>4 q8 q8 <d' f'>2 }
  \layout {}
}
