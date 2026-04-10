import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        # 使用一組更像真人的啟動參數
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--disable-http2", 
                "--disable-blink-features=AutomationControlled",
                "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
            ]
        )
        
        # 設定香港當地的語言和時區
        context = await browser.new_context(
            locale="zh-HK",
            timezone_id="Asia/Hong_Kong",
            viewport={'width': 1920, 'height': 1080}
        )
        
        page = await context.new_page()

        try:
            print("正在以偽裝模式進入國泰兌換頁面...")
            # 關鍵：直接跳轉到一個較輕量的入口
            url = "https://www.cathaypacific.com/cx/zh_HK/book-a-trip/redeem-flights.html"
            
            # 使用 wait_until="commit" 避免被廣告或追蹤腳本拖慢導致超時
            await page.goto(url, wait_until="commit", timeout=60000)
            
            # 模擬人類等待：不要立刻操作，先停 15 秒讓 Akamai 防禦降低警戒
            print("頁面已連線，模擬真人閱讀中...")
            await asyncio.sleep(15)
            
            # 嘗試截取第一張圖，確認是否看到搜尋框
            await page.screenshot(path="github_result.png")
            print("✅ 初始截圖已完成")

            # 如果截圖顯示有內容，我們就可以在此加入 fill("HKG") 等邏輯
            
        except Exception as e:
            print(f"❌ 依然發生錯誤: {e}")
            try:
                await page.screenshot(path="github_result.png")
            except:
                pass
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
