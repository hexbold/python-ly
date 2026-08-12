\version "2.24.0"
\language "english"
% FEATURE: \voiceX after the stream already carries music
% TESTS: a mid-stream \voiceTwo (stems/rests directive, e.g. around
%        cross-staff travel) must NOT renumber the MusicXML voice: the
%        stream would double-book the sibling voice's number and MuseScore
%        rejects the file (exit 40).
\score {
  \new Staff {
    \clef treble \key c \major \time 4/4
    <<
      \new Voice { \voiceOne c''4 d'' \voiceTwo e'' f'' }
      \new Voice { \voiceTwo g4 a b c' }
    >>
  }
  \layout {}
  \midi {}
}
