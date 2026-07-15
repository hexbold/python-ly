\version "2.24.0"

% <accidental> is a display element: "this notehead carries a printed
% accidental". The sounding pitch is fully described by <alter>, so a note
% already covered by the key signature must not emit one: doing that on
% every altered note forced a redundant printed flat/sharp on every
% key-signature-covered note. Explicit ! (forced) and ? (cautionary) always
% emit. Where an accidental IS notated is decided by the accidental rule,
% covered in accidental_rule.ly.

\score {
  \new Staff {
    \key ees \major \time 4/4
    bes4 ees' aes' g' |
    ees'!4 aes'? bes'2
  }
  \layout { }
}
