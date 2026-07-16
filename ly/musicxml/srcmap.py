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
Source-map (provenance) collection for the MusicXML export.

Enabled with ``ly.musicxml.writer(srcmap=True)``. While the exporter walks the
score and emits MusicXML, this collector records for every emitted object that
exists as a real token in the parsed LilyPond text WHERE in that text it came
from, addressed the way the MusicXML (and a MusicXML renderer such as Verovio)
sees it: part index, measure number, voice number, event ordinal.

The map is a plain dict (JSON-serializable):

``parts``    one entry per ``<part>``: ``{"name": …, "staves": n}`` in part order.
``events``   one entry per emitted ``<note>`` (notes, rests, invisible skips),
             in emission order::

                 {"part": 0, "staff": 1, "measure": 1, "voice": 2,
                  "idx": 3, "member": 0, "kind": "note",
                  "pitch": {"step": "C", "alter": 0, "octave": 5},
                  "span": [start, end], "dur_span": [start, end],
                  "attach": [["artic", "staccato", start, end], …]}

             ``idx`` is the 0-based event ordinal within (measure, voice);
             chord members share their event's ``idx`` and count ``member`` up.
             ``span`` is the pitch region (note name + octave marks) in the
             parsed text; it is ABSENT for objects the exporter materialized
             without their own source token (``q`` repeats, ``R1*n`` copies,
             isolated durations) — those are not addressable for editing.
``objects``  standalone directives with a source token: ``\\tempo``, ``\\key``,
             ``\\time``, ``\\clef`` — ``{"part": …, "measure": …, "kind": …,
             "span": […], …extras}``.
``header``   ``\\header`` field name -> value span (the quoted string).

``positions_valid`` is False when the exporter parsed a CONVERTED copy of the
source (``\\relative`` input is converted to absolute pitches first) — spans
then index the converted text, not the text the caller supplied, and must not
be used for editing.
"""

from __future__ import unicode_literals


class SrcMapCollector():
    """Collects source spans while IterateXmlObjs emits the MusicXML."""

    def __init__(self, score):
        self._score = score
        self.parts = []
        self.events = []
        self.objects = []
        self._part = -1
        self._bar_nr = 1     # mirrors create_musicxml.CreateMusicXML numbering
        self._measure = 0
        self._ords = {}      # voice -> last event ordinal in the current measure
        self._last_event = None

    def start_part(self, name, staves):
        self._part += 1
        self.parts.append({"name": name or "", "staves": staves or 1})
        self._bar_nr = 1

    def start_measure(self, pickup):
        # Exactly create_musicxml.create_measure's numbering: a pickup first
        # measure is number 0 (implicit), counting continues from 1.
        if pickup and self._bar_nr == 1:
            self._bar_nr = 0
        self._measure = self._bar_nr
        self._bar_nr += 1
        self._ords = {}
        self._last_event = None

    def note(self, obj):
        self._event(obj, "note")

    def rest(self, obj):
        if obj.skip:
            kind = "skip"
        elif not obj.show_type:
            kind = "mrest"
        else:
            kind = "rest"
        self._event(obj, kind)

    def _event(self, obj, kind):
        voice = obj.voice or 1
        chord = bool(getattr(obj, "chord", False))
        if chord and self._last_event is not None \
                and self._last_event["voice"] == voice:
            idx = self._last_event["idx"]
            member = self._last_event["member"] + 1
        else:
            idx = self._ords[voice] = self._ords.get(voice, -1) + 1
            member = 0
        entry = {
            "part": self._part,
            "staff": obj.staff or 1,
            "measure": self._measure,
            "voice": voice,
            "idx": idx,
            "member": member,
            "kind": kind,
        }
        src = getattr(obj, "src", None)
        if src:
            entry["span"] = [src[0], src[1]]
        dur = getattr(obj, "src_dur", None)
        if dur:
            entry["dur_span"] = [dur[0], dur[1]]
        if kind == "note":
            # alter can be a Fraction (get_xml_alter returns the exact value when
            # integral) — normalize so the map is JSON-serializable
            alter = obj.alter
            alter = int(alter) if float(alter).is_integer() else float(alter)
            entry["pitch"] = {
                "step": obj.base_note,
                "alter": alter,
                "octave": obj.octave,
            }
            if obj.grace[0]:
                entry["grace"] = True
            if getattr(obj, "src_transposed", False):
                # sounding pitch differs from the written source token (\transpose)
                entry["transposed"] = True
        attach = getattr(obj, "src_attach", None)
        if attach:
            entry["attach"] = [[k, n, s, e] for (k, n, s, e) in attach]
        self._last_event = entry
        self.events.append(entry)

    def bar_attr(self, obj):
        if obj.key is not None:
            self._object("key", getattr(obj, "src_key", None),
                         fifths=obj.key, mode=obj.mode)
        if obj.time:
            self._object("time", getattr(obj, "src_time", None),
                         time=list(obj.time)[:2])
        if obj.clef:
            self._object("clef", getattr(obj, "src_clef", None))
        for mc in obj.multiclef:
            if len(mc) > 2 and mc[2]:
                self._object("clef", mc[2], staff=mc[1])
        if obj.tempo is not None:
            self._object("tempo", getattr(obj.tempo, "src", None))

    def _object(self, kind, src, **extras):
        if not src:
            return
        entry = {
            "part": self._part,
            "measure": self._measure,
            "kind": kind,
            "span": [src[0], src[1]],
        }
        entry.update(extras)
        self.objects.append(entry)

    def result(self, positions_valid=True):
        header = {}
        for name, src in getattr(self._score, "src_header", {}).items():
            if src:
                header[name] = [src[0], src[1]]
        return {
            "v": 1,
            "positions_valid": bool(positions_valid),
            "parts": self.parts,
            "events": self.events,
            "objects": self.objects,
            "header": header,
        }
