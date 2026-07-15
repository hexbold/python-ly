\version "2.24.0"

% Header metadata must produce a schema-valid <identification>: creator before
% rights, ahead of the <encoding> block. Two regressions guarded here:
% (1) a Scheme header value stringifies to '' (the ubiquitous tagline = ##f) and
%     used to emit an EMPTY <rights/> — empty values must be skipped;
% (2) create_score_info PREPENDED elements, so <rights> landed before <creator>,
%     which the identification sequence forbids.

\header {
  title = "Header Order"
  composer = "A. Composer"
  tagline = ##f
  copyright = "2026"
}

\score {
  { \time 4/4 c'4 d'4 e'4 f'4 }
  \layout {}
}
