\version "2.18.2"

melody = { \key c \major \time 4/4 c'4 d'4 e'4 f'4 | g'1 | }
accomp = { \clef bass \key c \major \time 4/4 c2 g,2 | c1 | }

\score {
  <<
    \new Staff { \tempo 4 = 72 \new Voice = "mel" \melody }
    \new Staff \accomp
  >>
  \layout {}
  \midi {}
}
