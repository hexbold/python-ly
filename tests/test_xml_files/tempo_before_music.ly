\version "2.24.0"

% \tempo followed directly by music: the tempo reader's token loop never
% stopped, so a chord (or variable reference) after "\tempo 4 = 132"
% re-entered deeper lexer states and was silently consumed — the first
% chord vanished and the measure boundaries broke. Also covers the
% text-only form, which had the same gap before the equal sign.

melody = {
  \time 4/4
  \tempo "Vivo" 4 = 132 <c' e' g'>4 d'4 e'4 f'4 |
  \tempo "Adagio" <g' b' d''>2 g'2
}

\score {
  \new Staff \melody
  \layout { }
}
