\version "2.24.0"
\language "english"

"mel.1" = { a'4 b'8 c''8 d''4 e''4 }
"mel.2" = { d''4 c''8 b'8 a'2 }

melody = { \clef treble \key a \minor \time 4/4 \"mel.1" | \"mel.2" | }

\score {
  \new Staff \melody
  \layout {}
  \midi {}
}
