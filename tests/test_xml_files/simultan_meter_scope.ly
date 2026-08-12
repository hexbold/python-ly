\version "2.24.0"
\language "english"
% FEATURE: \time change inside one voice of a << .. >> group
% TESTS: sections are parsed sequentially, but parallel voices all start at
%        the same musical moment — the meter one voice ends in must not leak
%        into the bar accounting of the NEXT voice (its bars closed on the
%        wrong sums from bar 1, mincing the whole part into pseudo-bars).
\score {
  \new Staff {
    \time 4/4
    <<
      \new Voice { \voiceOne c'4 d' e' f' | \time 3/8 g'8 a' b' }
      \new Voice { \voiceTwo e4 f g a | \time 3/8 e8 f g }
    >>
  }
  \layout {}
  \midi {}
}
