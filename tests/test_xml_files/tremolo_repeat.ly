\version "2.24.0"

% \repeat tremolo. calc_trem_dur reached for durval2type in xml_objs, where it does not
% live; the AttributeError was swallowed by the item dispatch, so the duration rewrite
% never ran and the whole tremolo collapsed to its written note pair.
%
% Bar 1  two-note tremolo: each note is WRITTEN with the whole span (two whole notes) and
%        sounds for half of it, hence time-modification 2/1, with start/stop markers.
% Bar 2  single-note tremolo via \repeat: one half note, marker type single, no
%        time-modification. Braces do not make it a two-note tremolo; two notes do.
% Bar 3  the colon spelling, for contrast.

\score {
  \new Staff {
    \time 4/4
    \repeat tremolo 8 { c'16 g'16 } |
    \repeat tremolo 8 { c'16 } c'2 |
    c'1:16 |
  }
  \layout { }
}
