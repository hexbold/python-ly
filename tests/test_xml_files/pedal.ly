\version "2.24.0"

% Sustain pedal marks must become <direction-type><pedal type="start|stop">
% directions at the note's position. Both used to fall through the command
% dispatcher as "Unknown command" and vanish.

\score {
  { \time 4/4 c'2\sustainOn d'2 e'2\sustainOff f'2 }
  \layout {}
}
