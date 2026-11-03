# Dirty South Trivia Show Vault: mandatory production rules

This file governs every show cockpit under `dst-archive/`. These rules come from Lauren Bush. Treat them as acceptance criteria, not suggestions.

Canonical reusable Notion Skill: https://app.notion.com/p/40625df5cad18120a018c38c3ad316e6

## 1. Never shorten Matt's script
- Each edition's source is Matt Stephen's original Word document in Dropbox, typically `/Wild Heaven/Pub [number]/Pub Quiz [number].docx`.
- Read the ENTIRE original. Copy every spoken introduction, instruction, question, set of multiple-choice options, answer, category description, transition, pen-collection announcement, tiebreaker, hiring announcement, and closing **verbatim**. Do not paraphrase, trim, rewrite, or silently omit anything.
- Preserve all eight questions per numbered round with original answer explanations. Preserve the order and the original location of end-of-round instructions. Exact full script text appears under blue READ THIS labels. Full original host directions appear in separate purple HOST ONLY blocks, never reduced to a summary.
- Do not expose correct answers to players in the question body. Internet-only questions are not read aloud; confirm this week's answer at DirtySouthTrivia.com. Never reuse a past week's answer.
- Do not change Matt's wording to add phonetic guides. Put useful pronunciation guides in a separate yellow PRONOUNCE area immediately beside the relevant spoken words; proactively check the full packet.
- For video rounds, maintain the official original instructions, and embed a verified or user-supplied direct video link, not a YouTube search-result URL when direct link is known.

## 2. Mini-games are OPTIONAL and stay separate
- Lauren's DEFAULT is to SKIP mini-games. Her normal HOST next/previous controls must NEVER pass through any mini-game.
- Store ALL original mini-game material in the independent OPTIONAL GAMES tab. Include Matt's complete instructions, full sample spoken intros, rules, artist/music lists, prize criteria and directions, and any examples. Never paraphrase or remove those materials.
- Mini-games do not affect scored rounds or the scoreboard. They run only if Lauren explicitly decides to use them that night.

## 3. Protect prior shows and scores
- For each edition, create a unique dated folder with quiz number (for example `2026-10-27-648`), its own HTML, answer key, and score data. Never overwrite a prior edition or its teams.
- Use distinct localStorage keys and per-quiz server IDs. Confirm remote score API uses the correct quiz's score JSON.
- **Never assume** that the final round is always 2 points per correct. Read Matt's packet EACH week and confirm exact point value and Joker eligibility per round. For Quiz 648 (October 27, 2026) the packet explicitly says Round 6 is 2 points/correct, so 8 correct = 16 points before Joker; with R6 Joker, 32. The scoreboard stores raw ROUND POINTS (e.g. 6 R6 correct = enter 12), not the correct-answer count, and automatically adds Joker doubling. Label the points input clearly and do not double the raw score twice. Missing slips are blank, not zero.
- If grading photos live, respond briefly, follow the correct week's answer key, retain team names and Joker values, track unanswered/missing slips, and write scores only to that week's file.

## 4. QA before calling it finished
1. Compare the cockpit against Matt's entire current document section by section, including exact spoken wording and source answer notes. The only exceptions from normal HOST navigation are optional mini-games, which remain fully preserved in the OPTIONAL GAMES tab.
2. Check 6 rounds, 48 answers, full setup/rules, close and tiebreaker, end-of-round messages, accents/pronunciation, link to video, internet-only answer, Joker eligibility and points.
3. Open HOST: check navigation goes only through the actual show, with no mini-games. Open OPTIONAL GAMES separately and confirm the full original instructions. Check SCORE still works.
4. Verify the deployed website actually shows the latest commit and that old show links still work. Never report 'live' solely because GitHub source was saved.
5. If anything is missing or differs from source, state it explicitly and fix it before claiming a finished show.

## Active reference
Show Vault: https://dirty-south-trivia-show-vault.onrender.com/
Halloween show 648 (2026-10-27): https://dirty-south-trivia-show-vault.onrender.com/2026-10-27-648/

## 5. Host-stage microphone script and category convention (Lauren's November 3 correction)
- **Every scored round must display a prominent heading: `CATEGORY: <exact round title>`**, before the spoken questions or introduction. This is a standard operating requirement for every weekly edition.
- The active on-mic content must read like a real host script that Lauren can say naturally without mental translation. Label it **READ ALOUD** or **READ THIS**; never put an internal packet instruction such as "don't read this question" in the on-mic reading box.
- **Internet-only Question 1:** provide a short spoken prompt inviting players to find the question at DirtySouthTrivia.com. Keep Matt's original internal direction verbatim in a collapsed host-only reference, with the official answer hidden until reveal.
- **Weekly rules:** build one clear spoken Joker explanation from this week's *specific* round headers. For Pub 650 only, Joker is permitted in R1–R4, not in Guess Who/R5 or R6. No contradictory general Joker text should appear in the active host notes. Preserve Matt's conflicting boilerplate word-for-word in a collapsed reference labeled "Original Matt packet wording".
- Preserve all original source sentences in the edition's archived original document or transcript. For the few sections Lauren explicitly requests be adapted into microphone-ready language, put the complete original behind an expandable reference and show the cleaned-up spoken version by default. Otherwise do not edit or shorten any original spoken wording. Source archival fidelity and on-mic usability are both mandatory.
- For multiple-choice questions, Matt's actual question and all options belong together in the on-mic question box. Put separate yellow **HOST-ONLY PRONOUNCE** cues below, even for simple words. Reveal the correct option only on click. Never fabricate an extra explanation when the packet gives none.
- Before publishing, personally read the GO -> RULES -> ROUND 1 flow as a live emcee: can Lauren read it straight aloud without encountering notes, contradictory scoring claims, a leaked answer, or vague shorthand? Fix anything that fails.
