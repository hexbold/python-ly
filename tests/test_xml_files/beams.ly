\version "2.24.0"

% Beams. <accidental>'s sibling problem: <beam> is a notation element, and a consumer
% renders the beams it is given rather than working them out, so an export without them
% is a score of bare flagged notes. A source hardly ever writes beams with [ ], they come
% from LilyPond's automatic beaming, so ly/musicxml/beaming.py ports the rules from
% scm/lily/time-signature-settings.scm and scm/lily/auto-beam.scm.
%
% Bar 1  4/4 eighths beam in half-measure groups of four (beamExceptions 1/8 -> (4 4)).
% Bar 2  16ths fall through to the 1/12 exception and beam per quarter, with two levels.
% Bar 3  a quarter is never beamed; a rest cuts the run.
% Bar 4  a dotted eighth's sixteenth gets a backward hook, not a full second beam.
% Bar 5  manual [ ] wins over the rules.

\score {
  \new Staff {
    \time 4/4
    c'8 d' e' f' g' a' b' c'' |
    c'16 d' e' f' g' a' b' c'' d'' e'' f'' g'' a'' b'' c''' d''' |
    c'4 d'8 e' r8 f' g' a' |
    c'8. d'16 e'8. f'16 g'8. a'16 b'8. c''16 |
    c'8[ d' e'] f'[ g' a' b' c''] |
  }
  \layout { }
}
