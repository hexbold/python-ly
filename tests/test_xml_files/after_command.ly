\version "2.18.0"
\language "english"

music = { c'8 a d'16 c' b a \after 16 ^\f g'8. g'16 f'16 e' f' g' }

\score {
  \new Staff \music
  \layout {}
}
