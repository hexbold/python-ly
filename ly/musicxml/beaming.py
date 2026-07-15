# This file is part of python-ly, https://pypi.python.org/pypi/python-ly
#
# Copyright (c) 2008 - 2015 by Wilbert Berendsen
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# See http://www.gnu.org/licenses/ for more information.

"""
LilyPond's automatic beaming rules.

MusicXML <beam> is a notation element: a consumer renders the beams it is given and does
not work them out from the note values, so an export without <beam> is a score of bare
flagged notes. LilyPond decides beaming at layout time from the time signature, and a
source almost never spells beams out with [ ], so the rules have to be applied here to
know what the score actually looks like.

Ported from LilyPond 2.24:
  scm/lily/time-signature-settings.scm  the per-meter table and the default beat structure
  scm/lily/auto-beam.scm                default-auto-beam-check

Every meter is covered: those absent from the table fall back to the same default beat
structure LilyPond computes for them, so 7/8 behaves like LilyPond's 7/8 rather than like
nothing at all.
"""

from __future__ import unicode_literals

from fractions import Fraction


# scm/lily/time-signature-settings.scm: default-time-signature-settings. 'end' exceptions
# map a note length to the group sizes it beams in. Meters that "use defaults" upstream are
# deliberately absent here and are handled by beat_settings().
TIME_SIGNATURE_SETTINGS = {
    (2, 2): {'beamExceptions': {Fraction(1, 32): [8, 8, 8, 8]}},
    (2, 8): {'beamExceptions': {Fraction(1, 8): [2]}},
    (3, 2): {'beamExceptions': {Fraction(1, 32): [8, 8, 8, 8, 8, 8]}},
    (3, 4): {'beamExceptions': {Fraction(1, 8): [6], Fraction(1, 12): [3, 3, 3]}},
    (3, 8): {'beamExceptions': {Fraction(1, 8): [3]}},
    (4, 2): {'beamExceptions': {Fraction(1, 16): [4] * 8}},
    (4, 4): {'beamExceptions': {Fraction(1, 8): [4, 4], Fraction(1, 12): [3, 3, 3, 3]}},
    (4, 8): {'beatStructure': [2, 2]},
    (6, 4): {'beamExceptions': {Fraction(1, 16): [4] * 6}},
    (9, 4): {'beamExceptions': {Fraction(1, 32): [8] * 8}},
    (12, 4): {'beamExceptions': {Fraction(1, 32): [8] * 12}},
    (5, 8): {'beatStructure': [3, 2]},
    (8, 8): {'beatStructure': [3, 3, 2]},
}

# A note is beamable from the eighth downwards; MusicXML type name -> number of beams.
BEAM_COUNT = {
    "eighth": 1, "16th": 2, "32nd": 3, "64th": 4,
    "128th": 5, "256th": 6, "512th": 7, "1024th": 8, "2048th": 9,
}


def beat_settings(num, den):
    """(beat_base, beat_structure, beam_exceptions) in force for a num/den measure.

    The defaults are LilyPond's: beatBase is 1/den, and beatStructure groups the measure in
    threes when the numerator is greater than 3 and divisible by 3, otherwise in single base
    moments. That is what makes 7/8 come out unbeamed, exactly as LilyPond engraves it.
    """
    settings = TIME_SIGNATURE_SETTINGS.get((num, den), {})
    if num > 3 and num % 3 == 0:
        default_structure = [3] * (num // 3)
    else:
        default_structure = [1] * num
    return (Fraction(1, den),
            settings.get('beatStructure', default_structure),
            settings.get('beamExceptions', {}))


def _ending_moments(group_list, base):
    """The measure positions at which each group in group_list ends."""
    moments, total = [], 0
    for group in group_list:
        total += group
        moments.append(base * total)
    return moments


def beam_ends_at(pos, length, num, den):
    """Must a beam of notes of `length` end at measure position `pos`?

    Port of end? in default-auto-beam-check. `length` is the note's actual, scaled length,
    so a triplet eighth is 1/12 and is matched by the 1/12 exceptions in the table.
    """
    beat_base, beat_structure, exceptions = beat_settings(num, den)
    period = beat_base * sum(beat_structure)
    pos = pos % period
    if pos == 0:
        return True
    grouping = exceptions.get(length)
    moment = length
    if not grouping:
        # An exception given for a longer note also governs shorter ones.
        larger = sorted(k for k in exceptions if k >= length)
        if larger:
            moment = larger[0]
            grouping = exceptions[moment]
    if grouping:
        return pos in _ending_moments(grouping, moment)
    return pos in _ending_moments(beat_structure, beat_base)


def beam_states(counts):
    """Beam levels for one group of notes, given each note's number of beams.

    Returns a list of [(number, state), ...] per note, where state is begin/continue/end or
    a hook for a level the note does not share with either neighbour (the 16th of a dotted
    eighth pair).
    """
    out = []
    for i, count in enumerate(counts):
        prev_count = counts[i - 1] if i > 0 else 0
        next_count = counts[i + 1] if i < len(counts) - 1 else 0
        states = []
        for nr in range(1, count + 1):
            has_prev, has_next = prev_count >= nr, next_count >= nr
            if has_prev and has_next:
                state = "continue"
            elif has_next:
                state = "begin"
            elif has_prev:
                state = "end"
            else:
                state = "forward hook" if i == 0 else "backward hook"
            states.append((nr, state))
        out.append(states)
    return out
