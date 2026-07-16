\version "2.24.0"

% LilyPond's \lyricsto melisma rule: notes continuing a slur or a tie take
% no syllable of their own. Only the __ extend used to trigger the skip, so
% a plain slurred melisma shifted every following syllable one note early.

\score {
  \new Staff <<
    \new Voice = "mel" { \time 4/4 c'4( d'4) e'4~ e'4 g'2( a'4 b'4) }
    \new Lyrics \lyricsto "mel" { one two three }
  >>
  \layout {}
}
