\version "2.24.0"

% A \lyricsto Lyrics context written as a SIBLING of the staff (the idiomatic
% song layout) must still find its voice. The voice's section is already merged
% into its part — and gone from the mediator's active sections — by the time the
% lyrics are parsed, so the lookup needs the named-section registry. This shape
% used to drop every lyric with "Warning can't merge in lyrics! None"; only the
% variant with the Lyrics context inside the staff's << >> worked.

\score {
  <<
    \new Staff {
      \new Voice = "mel" { \time 4/4 c'4 d'4 e'4 f'4 }
    }
    \new Lyrics \lyricsto "mel" { one two three four }
  >>
  \layout {}
}
