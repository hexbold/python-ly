\version "2.24.0"
\language "english"
% FEATURE: ties that LilyPond drops must not survive as dangling starts
% TESTS: (1) chord tied into a single note - only the matching pitch keeps
%        its tie, the other members' starts are pruned (readers tied them to
%        whatever same-pitch note came bars later);
%        (2) tie into a rest dies entirely;
%        (3) a grace note between a tie and its target neither consumes nor
%        stops the tie.
\score {
  \new Staff {
    \clef treble \key c \major \time 4/4
    <b' e'' g''>4~ e''16 d'' e'' d'' e''2 |
    c''2~ r4 c''4 |
    c''2~ \grace { d''8 } c''2 |
  }
  \layout {}
  \midi {}
}
