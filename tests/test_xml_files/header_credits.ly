\version "2.24.0"

% Renderers that draw the page header from <credit> blocks (Verovio, MuseScore)
% show only the title without them — the composer would exist merely as
% <identification> metadata. Every header field must yield its credit;
% MusicXML's credit vocabulary has no "poet", it maps to lyricist.

\header {
  title = "Credit Test"
  subtitle = "The Subtitle"
  composer = "A. Composer"
  poet = "A. Poet"
  arranger = "An. Arranger"
}

\score {
  \new Staff { c'4 d'4 e'4 f'4 | }
  \layout {}
}
