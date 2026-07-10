\version "2.24.0"

% A << >> that directly holds staff/group contexts is score STRUCTURE,
% not simultaneous music, and must not open a music section: each staff
% end already consumes a section when more than one is open, so the
% sections opened for structural << >> underflowed the stack — a score
% with two StaffGroup << >> blocks crashed in check_simultan
% (IndexError: pop from empty list).

flute = { \clef treble \time 4/4 c''4 d'' e'' f'' | g''1 }
oboe = { \clef treble \time 4/4 e''4 f'' g'' a'' | b''1 }
cello = { \clef bass \time 4/4 c4 e g c' | c1 }

\score {
  <<
    \new StaffGroup <<
      \new Staff \flute
      \new Staff \oboe
    >>
    \new StaffGroup <<
      \new Staff \cello
    >>
  >>
  \layout { }
}
