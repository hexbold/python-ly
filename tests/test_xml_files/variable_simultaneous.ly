\version "2.18.0"

upone = { c''4 d''4 e''4 f''4 }
uptwo = << { a''2 b''2 } \\ { c''2 d''2 } >>
upthree = { g''4 f''4 e''4 c''4 }
upper = { \clef treble \time 4/4 \upone | \uptwo | \upthree | }
\score {
  \new Staff \upper
  \midi {}
}
