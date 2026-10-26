"""Streamlit 앱이 잠들지 않도록 페이지를 열고, 잠들어 있으면 깨웁니다.

정상적으로 페이지가 뜨지 않으면 종료 코드 1로 끝나서 GitHub Actions가 실패로 표시하고
저장소 소유자에게 알림 메일을 보냅니다.
"""
import re
import sys

from playwright.sync_api import sync_playwright

URL = "https://acm-event.streamlit.app/"
EXPECTED_TEXT = "AccessMedicine"   # 앱이 정상적으로 떴을 때 화면에 있는 문구
WAKE_BUTTON = re.compile(r"get this app back up", re.I)


def page_has_app(page) -> bool:
    for frame in page.frames:
        try:
            if EXPECTED_TEXT in (frame.inner_text("body", timeout=2000) or ""):
                return True
        except Exception:
            pass
    return False


def main() -> int:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto(URL, wait_until="domcontentloaded", timeout=120_000)
        page.wait_for_timeout(10_000)

        woke = False
        button = page.get_by_role("button", name=WAKE_BUTTON)
        if button.count():
            print("앱이 잠들어 있어 깨우는 중...")
            button.first.click()
            woke = True

        # 최대 3분 동안 앱 화면이 뜨는지 확인
        for _ in range(36):
            if page_has_app(page):
                print("앱이 다시 깨어났습니다." if woke else "앱이 정상적으로 깨어 있습니다.")
                browser.close()
                return 0
            page.wait_for_timeout(5_000)

        page.screenshot(path="keep_awake_failure.png", full_page=True)
        print("앱 화면을 확인하지 못했습니다.", file=sys.stderr)
        browser.close()
        return 1


if __name__ == "__main__":
    sys.exit(main())
