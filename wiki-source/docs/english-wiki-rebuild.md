# English wiki rebuild — 18 September 2026

The entire published wiki now uses English editorial content and a traditional article layout: a persistent navigation sidebar, compact page navigation, serif article headings, contents lists, reference boxes and ordinary linked tables. The home page is a directory, not a long guide. The layout follows familiar MediaWiki conventions while retaining Zenith branding and custom server documentation.

Coverage: 800 independently addressable articles, including all 94 previous article URLs, 18 camp walkthroughs, 689 linked catalogue item references, city and field zone guides, NPC pages and individual quest walkthroughs. The three old preview URLs redirect to their corresponding current pages; old home-page section bookmarks retain their route mapping.

English source is maintained in `content/english/articles.py`; source camp and market records remain authoritative inputs. Generated output lives in `dist`. Historical bilingual source is retained for editorial traceability and is not deployed. Retired public styles and scripts were removed. Every page uses the same current stylesheet and interaction script.

The redesign does not install server packages or modify game rules. Ready/unconfirmed status is preserved for NPC Roles, Qufim Wall, Menu Pages, Trust Recovery v1.1, Road Companion and Auction Market. Market pages show package prices, never live stock. The Gausebit page explicitly notes its absence from the 689-item catalogue. Item references do not invent equipment stats unavailable in the catalogue.

Validation: all HTML is English, one shared layout across every article, no duplicate IDs, no missing local link or asset targets, all previous articles retained, search index and directory cover every article, all 689 catalogue rows match the source exactly, all 18 camps retained. Key quest materials, levels, rewards and market caps checked. JavaScript syntax validated. This plain static Site has no compatible supervised browser-preview server; no live browser screenshot review was performed.
