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

        # フライトプラン登録サービスへ
        page.goto("https://web.swim.mlit.go.jp/f1fprg/browse/fia627s010")

        page.wait_for_timeout(15000)

        print("FPL URL:", page.url)

        content = page.content()

        print("通報一覧:", "通報一覧" in content)

        # HTML保存
        with open("fpl_page.html", "w", encoding="utf-8") as f:
            f.write(content)

        print("FPLページ保存完了")

        # aタグ一覧確認
        links = page.locator("a")

        count = links.count()

        print("リンク数:", count)

        for i in range(min(count, 30)):
            try:
                text = links.nth(i).text_content()
                href = links.nth(i).get_attribute("href")

                print(
                    f"{i}: text={text} href={href}"
                )

            except Exception as e:
                print(
                    f"{i}: ERROR={e}"
                )

        page.screenshot(
            path="fpl_page.png",
            full_page=True
        )
        
        cards = page.locator("swim-card2")
        
        print("カード数:", cards.count())
        
        cards.nth(1).click()
        
        page.wait_for_timeout(15000)
        
        print("クリック後URL:", page.url)
        
        content = page.content()
        
        print("JA6502:", "JA6502" in content)
        
        with open(
            "notification_list.html",
            "w",
            encoding="utf-8"
        ) as f:
            f.write(content)
            
            page.screenshot(    
                path="notification_list.png",
                full_page=True
            )
            print("通報一覧保存完了")
            print("スクリーンショット保存完了")

        browser.close()


if __name__ == "__main__":
    run()
