\version "2.18.0"
\language "english"

music = { c'16 d' \tuplet 3/2 8 { e'16 f' g' } \tuplet 3/2 8 { a' g' f' } e'4 d'4 c'4 }

\score {
  \new Staff \music
  \layout {}
}
