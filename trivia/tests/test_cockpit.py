"""Browser QA for the existing Dirty South Trivia cockpit. No redesigns."""
import html
import json
import subprocess
import re
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
LIVE = ROOT / "trivia" / "current"

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args): pass

def require(ok, reason):
    if not ok: raise AssertionError(reason)

def static_checks():
    cockpit = (LIVE / "index.html").read_text(encoding="utf8")
    launcher = (LIVE / "scorekeeper.html").read_text(encoding="utf8")
    match = re.search(r"Pub\s+(\d+)", cockpit)
    require(bool(match), "Current quiz number missing")
    number = match.group(1)
    classic = 'data-tab="host"' in cockpit
    require('class="scorechat-top"' in cockpit, "Top START SCORE CHAT missing")
    require("scorechat-host" in cockpit, "HOST START SCORE CHAT missing")
    require("#ff4dab" in cockpit.lower() and "#baff72" in cockpit.lower(), "Original pink/green identity missing")

    if classic:
        data_match = re.search(r'<script>const DATA=(\{[\s\S]*?\});</script>', cockpit)
        require(bool(data_match), "Classic shell DATA missing")
        data = json.loads(data_match.group(1))
        require(len(data["stages"]) == 9, "Classic HOST requires nine stages")
        for idx in [2,3,4,7]:
            require(len(data["stages"][idx].get("qs", [])) == 8, f"Stage {idx+1} missing questions")
        require(len(data["stages"][5].get("answers", [])) == 8, "Video round missing answers")
        require(len(data["stages"][6].get("clues", [])) == 5, "Round 5 missing clues")
        scripts = re.findall(r"<script>([\s\S]*?)</script>", cockpit)
        for i, script in enumerate(scripts):
            result = subprocess.run(["node", "--check", "-"], input=script, text=True, capture_output=True)
            require(result.returncode == 0, f"Script {i+1} syntax error: {result.stderr}")
        require('id="next"' in cockpit and 'id="body"' in cockpit, "Classic HOST/NEXT controls missing")
        require('id="startScoreChat"' in cockpit, "Classic SCOREBOARD chat button missing")
    else:
        require(cockpit.count("START SCORE CHAT") >= 3, "Expected top, HOST and SCOREBOARD chat controls")
        for idx in range(9):
            require(f'id="step{idx}"' in cockpit, f"Stage {idx+1} missing")
        for idx in (2,3,4,5,7):
            part = cockpit.split(f'id="step{idx}"',1)[1].split("</section>",1)[0]
            require(part.count('class="question-card"') == 8, f"Stage {idx+1}: missing questions")
        clues = cockpit.split('id="step6"',1)[1].split("</section>",1)[0]
        require(clues.count('class="question-card"') == 5, "Round 5 needs five clues")

    target = re.search(r'<a[^>]*id="go"[^>]*href="([^"]+)"', launcher)
    require(bool(target), "Scorekeeper launch button missing")
    parsed = urlparse(html.unescape(target.group(1)))
    prompt = parse_qs(parsed.query).get("q", [""])[0]
    require(parsed.netloc == "chatgpt.com", "Scorekeeper does not open ChatGPT")
    require(f"Pub Quiz {number}" in prompt, "Scorekeeper prompt has wrong quiz number")
    require("laurenbush305.github.io/scrambled-up-practice/trivia/current/" in prompt, "Prompt has obsolete host URL")
    require("dirty-south-trivia-show-vault.onrender.com" not in prompt, "Render URL in active prompt")
    print(f"PASS static: Pub {number}, {'classic' if classic else 'native'} UI, data, chat")


def browser_checks(browser, base, width, blocked=False, launch=False):
    context = browser.new_context(viewport={"width":width,"height":850})
    if blocked:
        context.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new Error('storage blocked')}})")
    context.route("https://chatgpt.com/**", lambda route: route.fulfill(status=200, content_type="text/html", body="QA interception"))
    page = context.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(base+"trivia/current/index.html", wait_until="domcontentloaded", timeout=25000)
    classic = page.locator('header button[data-tab="host"]').count() > 0
    host_tab = 'header button[data-tab="host"]' if classic else 'header label[for="tabHost"]'
    host_chat = '#host a.scorechat-host' if classic else '#viewHost a.scorechat-host'
    require(page.locator(host_tab).is_visible(), "HOST control missing")
    require(page.locator('header a.scorechat-top').is_visible(), "Top scorekeeping launcher missing")
    require(page.locator(host_chat).is_visible(), "HOST scorekeeping launcher missing")
    pink = page.locator(host_tab).evaluate("(e)=>getComputedStyle(e).backgroundColor")
    require(pink == "rgb(255, 77, 171)", "HOST lost pink styling")
    green = page.locator('header a.scorechat-top').evaluate("(e)=>getComputedStyle(e).backgroundColor")
    require(green == "rgb(186, 255, 114)", "Chat launcher lost green styling")

    if classic:
        require("Welcome" in page.locator('#category').inner_text(), "Welcome not loaded")
        page.locator('#next').click()
        require("How tonight works" in page.locator('#category').inner_text(), "NEXT to rules failed")
        page.locator('#next').click()
        require("Random" in page.locator('#category').inner_text(), "NEXT to Round 1 failed")
        require(page.locator('#body article.q').count() == 8, "Round 1 missing questions")
        reveal = page.locator('#body details.answer').first
        require(reveal.get_attribute("open") is None, "Answer leaked")
        reveal.locator('summary').click()
        require(reveal.get_attribute("open") is not None, "Answer reveal failed")
        reveal.locator('summary').click()
        require(reveal.get_attribute("open") is None, "Answer hide failed")
        page.locator('#back').click()
        require("How tonight works" in page.locator('#category').inner_text(), "BACK failed")
        page.locator('#jumpSelect').select_option("7")
        require("Toy With Your Food" in page.locator('#category').inner_text(), "JUMP to Round 6 failed")
        page.locator('#restart').click()
        require("Welcome" in page.locator('#category').inner_text(), "START OVER failed")
        tabs = [('score','score'),('tie','tie'),('extras','extras')]
        for tab,panel in tabs:
            page.locator(f'header button[data-tab="{tab}"]').click()
            require(page.locator(f'#{panel}').is_visible(), f"{tab} did not open")
            page.locator(host_tab).click()
            require(page.locator('#host').is_visible(), f"HOST failed after {tab}")
        score_chat = '#score a#startScoreChat'
    else:
        require(page.locator('#step0').is_visible(), "Welcome not loaded")
        page.locator('#step0 label[for="stage1"]').click()
        require(page.locator('#step1').is_visible(), "NEXT to rules failed")
        page.locator('#step1 label[for="stage2"]').click()
        require(page.locator('#step2').is_visible(), "NEXT to Round 1 failed")
        require(page.locator('#step2 .question-card').count() == 8, "Round 1 missing questions")
        reveal = page.locator('#step2 details.answer').first
        require(reveal.get_attribute("open") is None, "Answer leaked")
        reveal.locator("summary").click()
        require(reveal.get_attribute("open") is not None, "Answer reveal failed")
        reveal.locator("summary").click()
        require(reveal.get_attribute("open") is None, "Answer hide failed")
        page.locator('#step2 label[for="stage1"]').click()
        require(page.locator('#step1').is_visible(), "BACK failed")
        page.locator('.hosttools .jump summary').click()
        page.locator('.hosttools .jumpmenu label[for="stage7"]').click()
        require(page.locator('#step7').is_visible(), "JUMP to Round 6 failed")
        page.locator('.hosttools label[for="stage0"]').click()
        require(page.locator('#step0').is_visible(), "START OVER failed")
        for tab,panel in [('tabScore','viewScore'),('tabTie','viewTie'),('tabExtras','viewExtras')]:
            page.locator(f'header label[for="{tab}"]').click()
            require(page.locator(f'#{panel}').is_visible(), f"{tab} did not open")
            page.locator(host_tab).click()
            require(page.locator('#viewHost').is_visible(), f"HOST failed after {tab}")
        score_chat = '#viewScore a.scorechat-host'

    if launch:
        for selector in ['header a.scorechat-top',host_chat]:
            with page.expect_popup(timeout=7000) as out:
                page.locator(selector).click()
            popup=out.value
            popup.wait_for_url(re.compile(r"scorekeeper\.html|chatgpt\.com"), timeout=7000)
            popup.close()
        if classic:
            page.locator('header button[data-tab="score"]').click()
        else:
            page.locator('header label[for="tabScore"]').click()
        with page.expect_popup(timeout=7000) as out:
            page.locator(score_chat).click()
        out.value.close()

    require(not errors, "Browser JS errors: "+"; ".join(errors))
    context.close()
    print(f"PASS browser: {width}px, {'classic' if classic else 'native'}, storage {'blocked' if blocked else 'normal'}, HOST/NEXT/BACK/JUMP/REVEAL/CHAT")


def main():
    static_checks()
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT)))
    worker=threading.Thread(target=server.serve_forever,daemon=True)
    worker.start()
    base=f"http://127.0.0.1:{server.server_address[1]}/"
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True)
            try:
                for width in [1366,390]:
                    for blocked in [False,True]:
                        browser_checks(browser,base,width,blocked,launch=width==1366 and not blocked)
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()
    print("PASS all browser release checks; live public URL still requires separate QA.")

if __name__=="__main__":
    main()
