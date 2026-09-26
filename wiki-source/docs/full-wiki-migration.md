# Full wiki migration

The approved white and blue wiki layout now covers all 94 articles. The original
22 guide sections and source catalogue remain in `content/` for traceability.
Build with `python tools/build-wiki.py`; validate with `python tools/check-wiki.py`.

- Independent articles for documented quests, jobs, travel, trusts, launcher,
  items, economy and camp guidance.
- 18 camp walkthroughs use the existing Quest Tidy catalogue, with 12 zone indexes.
- The 689-entry starter market catalogue is retained, with item search.
- Shared navigation, full-article search, camp level filtering, article contents,
  breadcrumbs and related links. English names and Arabic walkthroughs.
- Existing root section bookmarks and the three preview URLs resolve to the new
  articles. Apururu's reviewed map and checklist remain available.

Validation checks 97 HTML routes, local links/assets/fragments, page coverage,
heading language, 18 camp rows, and 689 market rows. JavaScript syntax is checked
with Node. This static project has no supported supervised browser preview;
these checks do not constitute a browser screenshot comparison.

The site documents existing source packages and observed screenshots. It is not
connected to the live game server. Package readiness is not an assertion that an
installer was run on the user's Windows computer. Map grids are included only
where a verified reference exists; camp world coordinates are labelled as such.
