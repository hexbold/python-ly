\version "2.24.0"

% Two \lyricsto contexts onto the same voice are two verses: their lyrics
% must be numbered lyric number="1" and number="2" per note. Both used to
% be numbered "1", so consumers could not stack them.

\score {
  \new Staff <<
    \new Voice = "mel" { \time 4/4 c'4 d'4 e'4 f'4 }
    \new Lyrics \lyricsto "mel" { one two three four }
    \new Lyrics \lyricsto "mel" { five six sev -- en }
  >>
  \layout {}
}
