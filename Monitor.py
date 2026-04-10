import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        # 強制禁用 HTTP/2 避開協議錯誤，並模擬標配 Chrome 參數
        browser = await p.chromium.launch(
            headless=True, 
            args=["--disable-http2", "--no-sandbox"]
        )
        
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            viewport={'width': 1280, 'height': 800}
        )
        page = await context.new_page()

        try:
            print("開始連線國泰兌換頁面...")
            # 使用 commit 模式快速進入
            await page.goto("https://www.cathaypacific.com/cx/zh_HK/book-a-trip/redeem-flights.html", wait_until="domcontentloaded", timeout=60000)
            
            # 等待基礎結構載入
            await asyncio.sleep(8)
            
            # --- 自動填表邏輯 ---
            print("正在輸入搜尋資料 (HKG -> NRT)...")
            
            # 1. 輸入出發地 (預設通常是 HKG，但保險起見重新輸入)
            await page.click('button[data-testid="origin-input"]')
            await page.fill('input[aria-label="出發地"]', "HKG")
            await asyncio.sleep(1)
            await page.keyboard.press("Enter")

            # 2. 輸入目的地
            await page.click('button[data-testid="destination-input"]')
            await page.fill('input[aria-label="目的地"]', "NRT")
            await asyncio.sleep(1)
            await page.keyboard.press("Enter")

            # 3. 處理日期 (這部分最難，先嘗試直接點擊搜尋看預設日期，或截圖除錯)
            print("嘗試執行搜尋...")
            await page.click('button[type="submit"]')
            
            # 等待結果渲染
            await asyncio.sleep(10)
            
            # 截圖確認結果
            await page.screenshot(path="github_result.png", full_page=True)
            print("✅ 監控與截圖完成。")

        except Exception as e:
            print(f"❌ 運行錯誤: {e}")
            await page.screenshot(path="github_result.png") # 出錯也截圖看畫面
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
