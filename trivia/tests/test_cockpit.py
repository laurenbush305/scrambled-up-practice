"""Browser QA for the existing Dirty South Trivia cockpit. No redesigns."""
import html
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
    require('class="scorechat-top"' in cockpit, "Top START SCORE CHAT missing")
    require(cockpit.count("START SCORE CHAT") >= 3, "Need green score chat in header, HOST and SCOREBOARD")
    require("#ff4dab" in cockpit.lower() and "#baff72" in cockpit.lower(), "Original pink/green identity missing")
    for i in range(9):
        require(f'id="step{i}"' in cockpit, f"Missing host stage {i+1}")
    for i in [2,3,4,5,7]:
        stage = cockpit.split(f'id="step{i}"',1)[1].split("</section>",1)[0]
        require(stage.count('class="question-card"') == 8, f"Stage {i+1}: 8 questions/answers expected")
    clues = cockpit.split('id="step6"',1)[1].split("</section>",1)[0]
    require(clues.count('class="question-card"') == 5, "Round 5 needs five clues")
    target = re.search(r'<a[^>]*id="go"[^>]*href="([^"]+)"', launcher)
    require(bool(target), "Scorekeeper launch button not found")
    parsed = urlparse(html.unescape(target.group(1)))
    prompt = parse_qs(parsed.query).get("q",[""])[0]
    require(parsed.netloc == "chatgpt.com", "Scorekeeper does not open ChatGPT")
    require(f"Pub Quiz {number}" in prompt, "Scorekeeper prompt has wrong quiz number")
    require("laurenbush305.github.io/scrambled-up-practice/trivia/current/" in prompt, "Prompt has obsolete hosting URL")
    require("dirty-south-trivia-show-vault.onrender.com" not in prompt, "Render URL still in active prompt")
    print(f"PASS static: Pub {number}, questions, style, scorekeeper")

def browser_checks(browser, base, width, blocked=False, launch=False):
    context = browser.new_context(viewport={"width":width,"height":850})
    if blocked:
        context.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new Error('storage blocked')}})")
    context.route("https://chatgpt.com/**", lambda route: route.fulfill(status=200, content_type="text/html", body="QA interception"))
    page = context.new_page()
    errors=[]
    page.on("pageerror",lambda e: errors.append(str(e)))
    page.goto(base+"trivia/current/index.html",wait_until="domcontentloaded",timeout=25000)
    require(page.locator('header label[for="tabHost"]').is_visible(),"HOST control missing")
    require(page.locator('header a.scorechat-top').is_visible(),"Top scorekeeping launcher missing")
    require(page.locator('#viewHost a.scorechat-host').is_visible(),"HOST scorekeeping launcher missing")
    require(page.locator('#step0').is_visible(),"Welcome not shown on load")
    pink = page.locator('header label[for="tabHost"]').evaluate("(e)=>getComputedStyle(e).backgroundColor")
    require(pink == "rgb(255, 77, 171)", "HOST lost its pink styling")
    green = page.locator('header a.scorechat-top').evaluate("(e)=>getComputedStyle(e).backgroundColor")
    require(green == "rgb(186, 255, 114)", "Score chat lost its green styling")
    page.locator('#step0 label[for="stage1"]').click()
    require(page.locator('#step1').is_visible(), "NEXT to Rules failed")
    page.locator('#step1 label[for="stage2"]').click()
    require(page.locator('#step2').is_visible(), "NEXT to Round 1 failed")
    require(page.locator('#step2 .question-card').count()==8,"Round 1 missing questions")
    reveal=page.locator('#step2 details.answer').first
    require(reveal.get_attribute("open") is None, "Answer leaked before reveal")
    reveal.locator("summary").click()
    require(reveal.get_attribute("open") is not None, "Answer did not reveal")
    reveal.locator("summary").click()
    require(reveal.get_attribute("open") is None, "Answer did not hide")
    page.locator('#step2 label[for="stage1"]').click()
    require(page.locator('#step1').is_visible(), "BACK failed")
    page.locator('.hosttools .jump summary').click()
    page.locator('.hosttools .jumpmenu label[for="stage7"]').click()
    require(page.locator('#step7').is_visible(), "JUMP to Round 6 failed")
    page.locator('.hosttools label[for="stage0"]').click()
    require(page.locator('#step0').is_visible(), "START OVER failed")
    for tab, panel in [("tabScore","viewScore"),("tabTie","viewTie"),("tabExtras","viewExtras")]:
        page.locator(f'header label[for="{tab}"]').click()
        require(page.locator(f'#{panel}').is_visible(), f"{tab} did not open")
        page.locator('header label[for="tabHost"]').click()
        require(page.locator('#viewHost').is_visible(),f"HOST did not return after {tab}")
    if launch:
        for selector in ['header a.scorechat-top','#viewHost a.scorechat-host']:
            with page.expect_popup(timeout=6000) as out:
                page.locator(selector).click()
            popup=out.value
            popup.wait_for_url(re.compile(r"scorekeeper\.html|chatgpt\.com"),timeout=6000)
            popup.close()
        page.locator('header label[for="tabScore"]').click()
        with page.expect_popup(timeout=6000) as out:
            page.locator('#viewScore a.scorechat-host').click()
        out.value.close()
    require(not errors, "Browser JS errors: "+"; ".join(errors))
    context.close()
    print(f"PASS browser: {width}px, storage {'blocked' if blocked else 'normal'}, HOST/NEXT/BACK/JUMP/REVEAL/CHAT")

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
