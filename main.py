from playwright.sync_api import sync_playwright

SWIM_URL = "https://top.swim.mlit.go.jp/swim/login"

LOGIN_ID = "aak-opr@aerotoyota.co.jp"
LOGIN_PW = "@1234Dispatch"


def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        # ログイン
        page.goto(SWIM_URL)

        page.wait_for_timeout(10000)

        inputs = page.locator("input")

        print("input数:", inputs.count())

        inputs.nth(0).fill(LOGIN_ID)
        inputs.nth(1).fill(LOGIN_PW)

        page.locator("button").first.click()

        page.wait_for_timeout(15000)

        print("現在URL:", page.url)

        # フライトプラン登録サービスへ直接移動
        page.goto(
            "https://web.swim.mlit.go.jp/f1fprg/browse/fia627s010"
        )

        page.wait_for_timeout(15000)

        print("FPL URL:", page.url)

        content = page.content()

        print("通報一覧:", "通報一覧" in content)

        # FPL画面保存
        with open(
            "fpl_page.html",
            "w",
