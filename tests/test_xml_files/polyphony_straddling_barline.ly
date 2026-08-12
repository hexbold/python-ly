\version "2.24.0"
\language "english"
% FEATURE: inline << .. \\ .. >> polyphony block crossing a barline
% TESTS: a block that starts on beat 4 and ends on beat 1 of the NEXT bar
%        leaves a PARTIAL backup inside the second measure; the backup created
%        for the NEXT merged voice must still rewind to the measure start
%        (it summed since the last backup and came out short, overflowing the
%        measure and time-shifting every later voice and bar).
\score {
  \new Staff {
    \clef treble \key c \major \time 4/4
    <<
      \new Voice { \voiceOne
        c'4 c' c' << { d'8 e'8~ e'4 } \\ { g4~ g8 s8 } >> f'8 g' a'4 b'4 | c''1
      }
      \new Voice { \voiceTwo
        e4 e e e | e e e e | e1
      }
    >>
  }
  \layout {}
  \midi {}
}
