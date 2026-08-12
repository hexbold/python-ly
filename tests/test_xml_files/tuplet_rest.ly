\version "2.18.0"
\language "english"

music = { \tuplet 3/2 { c'8 d' r } \tuplet 3/2 { e'8 f' s8 } g'4 a'4 }

\score {
  \new Staff \music
  \layout {}
}
