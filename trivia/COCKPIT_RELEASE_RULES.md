# Dirty South Trivia cockpit: immutable weekly release contract

**READ THIS BEFORE TOUCHING THE COCKPIT EACH WEEK.** Updated November 17, 2026 after the Pub 654 deployment incident. Related Notion SOP: https://app.notion.com/p/40625df5cad18120a018c38c3ad316e6

## The user's actual request

"Update the cockpit" means **load the new official weekly question packet into the same established working cockpit**. Do not redesign the UI, introduce a new navigation scheme, use another host, or turn the host flow into a one-page script. The user has been hosting with this system for weeks, needs it reliable under live-show pressure, and does not consent to being the debugging/QA team.

**Permanent visual/interaction contract:**
- Original navy background, **pink** active HOST/tabs and NEXT/BACK controls, **green** START SCORE CHAT button.
- Keep **START SCORE CHAT** prominently in the TOP HEADER and the HOST TOOLBAR, and within SCOREBOARD. These are required controls, not decorative links.
- HOST shows the Welcome stage on load, and reopens the host panel after visiting another tab. NEXT/BACK move one stage, JUMP TO works, START OVER resets. Questions render within each round and official answers stay hidden until user reveals them.
- Normal HOST stages: Welcome, rules, Rounds 1–6, Winners + goodnight (9 stages for the current format). Tiebreaker lives ONLY in a separate tab and only for a prize-position tie. Optional mini-games live ONLY under OPTIONAL GAMES, not NEXT.
- READ ALOUD blue, PRONOUNCE yellow beside exact words (never reveal hidden answers), HOST ONLY purple, REVEAL ANSWER green. Preserve complete official Word source wording in the appropriate speaking/host-only area.
- Scoreboard and scorekeeper chat are distinct from the host flow. Keep the host usable even if the score feed, ChatGPT launcher, or local storage fails.

## Canonical sources and GitHub hosting

Repo: https://github.com/laurenbush305/scrambled-up-practice

- Official current-week source: the full Matt Stephen Word quiz packet under Dropbox `/Wild Heaven/Pub NNN/Pub Quiz NNN.docx` plus its related media. Read it in full and obey week-specific scoring and Joker rules.
- Classic UI reference: `dst-archive/2026-11-10-652/index.html` on branch `trivia-cockpit-644`, unless a more recently **user-accepted** classic cockpit supersedes it. This is a reference, not permission to overwrite previous editions.
- Build current week's dated source and answer key in `dst-archive/YYYY-MM-DD-NNN/` on `trivia-cockpit-644`.
- Publish the **same final approved content and working UI** on **main** at `trivia/YYYY-MM-DD-NNN/` and `trivia/current/`. Existing GitHub Pages already publishes from main; do not create a parallel Pages workflow or accidentally publish only the non-default branch.
- Permanent public entry: https://laurenbush305.github.io/scrambled-up-practice/trivia/current/
- Current-week scorekeeper launcher: `trivia/current/scorekeeper.html`; prompt must reference the exact week, server ID, answer key, and GitHub Pages URL. It must launch the current week's chat, not display wrong-week text. The launcher may contain a fallback, but don't claim auto-submission if unverified.
- Never change the repo's root `index.html` (Scrambled Up practice site) or unrelated projects.
- Do not use Render/Replit or ChatGPT attachments as primary hosting.

## Weekly process (no exceptions)

1. Open this file and the current Notion SOP before editing code.
2. Read the ENTIRE official current week's quiz packet, including internet-only answer, video rounds and mini-games. Compare against prior accepted cockpit.
3. Copy the accepted shell; edit the **DATA, answer key, dated labels, scoring parameters, prompt and IDs** only. Keep CSS, DOM, navigation and score chat button placement unchanged except for a necessary minimal compatibility repair.
4. Ensure the correct edition's answer-key/scores data are separated from prior weeks. Never carry forward teams or scores.
5. **Before publishing** parse all scripts with a JS parser and execute a real browser test for full HOST flow and all question/answer content. Syntax checks or mocked-DOM tests alone do not meet QA.
6. In a real laptop browser: click HOST, confirm Welcome, NEXT to Rules, NEXT to Round 1 with visible questions; use BACK, START OVER, JUMP TO Round 6, REVEAL and hide an answer, TIEBREAKER and back, OPTIONAL GAMES and back, SCOREBOARD and back.
7. Test the score chat entry points in HEADER, HOST and SCOREBOARD. Actually click to launch; verify new window/new thread and **correct current-edition** scoring prompt, including login/blocked-popup fallback. Do not call this "working" without a real launch test.
8. Test laptop and phone widths; test storage working and blocked. A localStorage exception must not prevent HOST or NEXT initialization. Confirm original pink/navy UI and prominent green chat buttons via screenshots/computed styles.
9. Publish to main on GitHub Pages in the dated and current folders. Wait for Pages success on the **final** commit and inspect the artifact to confirm the files at exact URL paths. Then open the **PUBLIC github.io URL** and repeat the key click tests on the published site; test link targets themselves rather than assuming GitHub green = working.
10. Validate score sync independently where supported: current GitHub scores JSON and public feed/dashboard must agree before saying "SYNCED".
11. Update the current Notion host record with packet, paths, score rules, link and verification receipts. Send ONE verified live GitHub Pages link and explain any genuinely unverified browser/destination behavior. Never make unsupported "fixed" claims.
12. Do not change the UI while troubleshooting. Isolate the smallest defect, repair it in-place, re-test and preserve a known-good rollback. No chaotic sequence of new hosting providers, one-page substitutes, redirect pages or surprise navigation changes.

## Nov. 17, 2026 Pub 654 failure: technical diagnosis and process lessons

- The Pub 654 video-round renderer had malformed JavaScript, preventing the entire UI from loading and all HOST/NEXT/BACK/tab handlers from attaching. Earlier deployment-success and mocked-DOM checks failed to catch the end-to-end failure.
- Browser storage failure was reported in a later Chromium test, so do not assume localStorage always works or allow it to gate host navigation.
- Render and Replit were needless hosting detours. GitHub Pages was already publishing from **main**. Copying to a trivia branch did not put the same code in the actual Pages artifact; a green Pages job was misleading without inspection.
- A static one-page version, CSS-only navigation rewrite, alternate URL paths, and new visual treatment were tried without user approval; these are not acceptable responses to a standard weekly update.
- The green START SCORE CHAT was removed/hidden from its established top and HOST positions during revisions, and the scorekeeper launcher temporarily referenced the obsolete Render cockpit. Restore and verify every entry point.
- Last corrective commit observed: `fc9d0d34f6c0f80b1c5140a60e2371075980f5cf` on main; Pages marked successful. **The user did not confirm operational acceptance** after that commit. Do not conflate deployment status with verified use.

**Release blocker:** if HOST cannot be clicked, NEXT does not advance, questions are missing, answer reveal fails, the green score-chat launcher doesn't launch the right edition, the public page cannot be verified, or the appearance deviates from the original without consent, the release is **NOT READY**.

## What should never happen again

A user should not have to repeatedly explain the same established UI, ask where HOST or START SCORE CHAT went, test dozens of new links, or watch an assistant change the site's identity as a shortcut. Never call a release ready until actual browser interaction and public hosting have been verified.
