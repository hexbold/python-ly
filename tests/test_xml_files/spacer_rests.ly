\version "2.24.0"

% Spacer rests (s and \skip) become INVISIBLE rests (print-object="no",
% the encoding MuseScore itself exports) - never printed rests, never
% <forward> gaps: a measure ENDING in a spacer used to emit a spurious
% measure-end <backup> (the empty-backup-list bug in is_skip) and the
% trailing forward-gap left the measure short in readers that derive
% measure length from content, shifting everything after it a beat early.

\score {
  { \time 4/4 c'4 s4 e'4 s4 \skip 4 f'4 g'2 }
  \layout {}
}
