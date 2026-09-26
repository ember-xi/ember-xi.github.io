# Installed-source documentation update — 19 September 2026

Evidence used for this content revision:

- User-provided source audit began at `2026-09-19T04:16:43.130230+00:00`. This is a file/settings audit, not a connection to the running Windows server or its database.
- User reported Phase 1 `zenith/menu-repair-v1/install-state.json` status `installed`. The reviewed installer writes that status after successful Map build/staging and source verification.
- User ran Phase 2 Status.cmd: `Phase 2 status: installed` and `INSTALLED AND VERIFIED: all 175 Phase 2 source files match.` In-game testing is explicitly deferred.
- Delivered Phase 2 archive SHA-256: `4640eff7ac90ec42aa2c7bbb1f37a7e953c438c28763b093f7303022f81161b9`.

Phase 2 waives 182 reviewed Fame eligibility predicates across 173 Lua files, makes the existing five 500-Sparks Ciphers permanently available, and retires the old reward-granting GM starter shortcut. It does not mutate character database records, change prices/EXP/gil settings, or alter the Apururu and Trust-capacity quests. The utility shop, ordinary weekly spending cap, vouchers and saved refund credits are retained.

The audit matched NPC Roles v1.0, Qufim Wall v1.0, Quest Tidy v1.1, Trust Recovery v1.1, Travel v1.1 and the Valkurm Ghoul source patch. Road Companion source and its installation record were present. Three Roads' helper and installation record were absent. An Auction Market installation record alone does not prove current worker/task operation or stock.

These distinctions belong in the Update Log and relevant article status notes. Do not relabel source verification as a fresh in-game test. Keep all existing routes and the English layout; the added Fame Access page has a separate URL. Catalogue prices and camp values were not changed in this revision.

## RoE Trust documentation review

- New roe-trusts article maps six objectives (932–937) to five Cipher rewards; final Joachim objective has no Cipher. Compared local roe_records.lua and individual Trust spell trigger scripts.
- Audited roe_sparks75.lua hash efa6e3ce111e48328270dff2b7f860e1d85605b59abac261b7ffafbf913ea398 allows 932–937 and excludes 1049 (Always Stand on 117).
- Full BG Wiki pages returned HTTP 403 in this review. Indexed BG Wiki entries corroborated the beginner objective/Cipher relationship; detailed server behavior comes from the local source snapshots. Do not represent those snapshots as a fresh runtime test or a complete audit of every retail Trust acquisition route.
- No server files or character records changed.
