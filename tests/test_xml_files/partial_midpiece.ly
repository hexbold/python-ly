\version "2.18.0"
\language "english"

music = { \time 2/4 \partial 4 \repeat volta 2 { c'4 | d'4 e' | f'4 } \repeat volta 2 { \partial 4 g'4 | a'4 b' | c''4 } }

\score {
  \new Staff \music
  \layout {}
}
