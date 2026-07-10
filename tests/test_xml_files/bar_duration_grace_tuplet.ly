\version "2.24.0"

% Bar-duration tracking regression test (grace notes + tuplets).
% Grace notes occupy no bar time; tuplet durations must be counted with
% their scaling applied. Unfixed code counted the grace's nominal
% duration and the tuplets' unscaled durations into the bar sum, closing
% the measure early and pushing the true last note(s) across the barline.

\score {
  <<
    % grace 1/8 (counted as real time when unfixed) + 3/4 + 1/8 reaches a
    % full 4/4 before e'8 -> e'8 was pushed into measure 2
    \new Staff { \time 4/4 \acciaccatura d'8 c'2. d'8 e'8 | f'1 }

    % two triplets counted unscaled = 6/8 instead of 4/8 -> the bar sum
    % reached 4/4 before a'4 -> a'4 was pushed into measure 2
    \new Staff { \time 4/4 \tuplet 3/2 { c'8 d' e' } \tuplet 3/2 { f'8 g' a' } g'4 a'4 | b'1 }
  >>
  \layout { }
}
