\version "2.24.0"

% A PianoStaff whose staves each hold explicit \new Voice contexts
% merges twice: the voices merge into their staff first, then End of
% the PianoStaff merges both staves into one part (with <backup>).
% The second merge hands is_skip() a bar that already contains a
% BarBackup, which has no has_attr() — this crashed with
% AttributeError: 'BarBackup' object has no attribute 'has_attr'.

upperOne = { g'4 f' e' d' | c'1 }
upperTwo = { e'4 d' c' b  | g1  }
lowerOne = { c4 d e f     | e1  }
lowerTwo = { c,1          | c,1 }

\score {
  \new PianoStaff <<
    \new Staff {
      \clef treble \time 4/4
      <<
        \new Voice \upperOne
        \new Voice \upperTwo
      >>
    }
    \new Staff {
      \clef bass \time 4/4
      <<
        \new Voice \lowerOne
        \new Voice \lowerTwo
      >>
    }
  >>
  \layout { }
}
