\version "2.18.0"
\language "english"

upper = { c''1 | c''1 | c''1 | c''1 }
lower = {
  e4 e e e |
  e2 << { g4 a } \\ { \voiceThree e2 } >> |
  << { g2~ g8 a b4 } \\ { \voiceThree s2 e4 << { \voiceTwo c'4 } \\ { \voiceFour e4 } >> } >> |
  e4 e e e
}

\score {
  \new PianoStaff <<
    \new Staff = "upper" { \clef treble \time 4/4 \upper }
    \new Staff = "lower" { \clef bass \time 4/4 \lower }
  >>
  \layout {}
}
