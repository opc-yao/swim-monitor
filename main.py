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

        # 利用サービス一覧へ
        page.click("text=利用サービス一覧")

        page.wait_for_timeout(10000)

        print("移動後URL:", page.url)

        # フライトプラン登録サービスが存在するか確認
        content = page.content()

        print(
            "フライトプラン登録サービス存在:",
            "フライトプラン登録サービス" in content
        )
        
        with open("service_list.html", "w", encoding="utf-8") as f:
            f.write(page.content())
        print("service_list.html 保存完了")

        page.get_by_text(
            "フライトプラン登録サービス"
        ).first.click()
        page.wait_for_timeout(10000)
        print("FPL移動後URL:", page.url)
        page.screenshot(
            path="fpl_service.png",
            full_page=True
        )
        print("FPL画面保存完了")

        # 検証用スクリーンショット
        page.screenshot(
            path="service_list.png",
            full_page=True
        )

        print("スクリーンショット保存完了")

        browser.close()


if __name__ == "__main__":
    run()
