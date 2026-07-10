\version "2.24.0"

% <accidental> is a display element: "this notehead carries a printed
% accidental". The sounding pitch is fully described by <alter>, and
% importers derive printed accidentals from <alter> + key signature +
% measure context. Emitting <accidental> on every altered note forced a
% redundant printed flat/sharp on every key-signature-covered note.
% Only explicit LilyPond accidentals may emit it: ! (forced) and
% ? (cautionary).

\score {
  \new Staff {
    \key ees \major \time 4/4
    bes4 ees' aes' g' |
    ees'!4 aes'? bes'2
  }
  \layout { }
}
