\version "2.24.0"
\language "english"

\score {
  <<
    \new Staff \with { midiInstrument = "oboe" } { c'1 }
    \new Staff \with { midiInstrument = "bassoon" } { c1 }
    \new Staff \with { midiInstrument = "french horn" } { c'1 }
    \new Staff \with { midiInstrument = "trumpet" } { c'1 }
    \new Staff \with { midiInstrument = "timpani" } { c1 }
    \new Staff \with { midiInstrument = "violin" } { c''1 }
    \new Staff \with { midiInstrument = "violin" } { c''1 }
    \new Staff \with { midiInstrument = "viola" } { c'1 }
    \new Staff \with { midiInstrument = "cello" } { c1 }
    \new Staff \with { midiInstrument = "contrabass" } { c,1 }
    \new Staff \with { midiInstrument = "harp" } { c'1 }
  >>
  \layout {}
  \midi {}
}
