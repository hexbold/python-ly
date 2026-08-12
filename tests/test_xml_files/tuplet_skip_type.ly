\version "2.24.0"
\language "english"
% FEATURE: spacer rest (skip) inside a \tuplet
% TESTS: the hidden rest must carry its written <type> (and dots): a tuplet
%        member with time-modification but no type is unreadable — the ratio
%        cannot be reconstructed — and MuseScore rejects the whole file.
\score {
  \new Staff {
    \clef treble \key c \major \time 4/4
    c'4 \tuplet 3/2 { d'8 s8 e'8 } \tuplet 2/3 { f'4 s4. } |
    c'1 |
  }
  \layout {}
  \midi {}
}
