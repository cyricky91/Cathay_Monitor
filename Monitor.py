import asyncio
import json
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # 監聽所有網路請求
        async def handle_response(response):
            # 尋找包含搜尋結果的 API 路徑（關鍵關鍵！）
            if "availability" in response.url or "search" in response.url:
                try:
                    data = await response.json()
                    print("✅ 發現機票數據 API!")
                    with open("result.json", "w") as f:
                        json.dump(data, f)
                except:
                    pass

        page.on("response", handle_response)

        try:
            print("正在連線國泰...")
            # 這裡填入你手動操作後得到的「直接搜尋 URL」會更有效
            await page.goto("https://www.cathaypacific.com/cx/zh_HK/book-a-trip/redeem-flights.html", wait_until="commit")
            
            # 模擬等待資料加載
            await asyncio.sleep(20) 
            
            await page.screenshot(path="github_result.png")
            print("監控任務完成。")
        except Exception as e:
            print(f"錯誤: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
