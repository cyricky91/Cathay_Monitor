import requests
import json
import time

def check_flights():
    # 這是國泰搜尋航班的核心 API (範例)
    url = "https://www.cathaypacific.com/cx/zh_HK/api/flight-availability.redeem.json"
    
    # 這裡是最關鍵的：偽裝成真實瀏覽器的 Headers
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Origin": "https://www.cathaypacific.com",
        "Referer": "https://www.cathaypacific.com/cx/zh_HK/book-a-trip/redeem-flights.html"
    }
    
    # 構造搜尋條件 (根據 NRT 2026-12-24 調整)
    payload = {
        "upsell": "true",
        "entryPoint": "REDEEM",
        "cabinClass": "ECONOMY",
        "destination": "NRT",
        "origin": "HKG",
        "travelDate": "20261224", # 日期格式需精確
        "tripType": "ONE_WAY",
        "adults": "1"
    }

    print(f"正在透過 API 查詢 HKG -> NRT (2026-12-24)...")
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        
        if response.status_code == 200:
            data = response.json()
            # 這裡解析 JSON 並判斷是否有位子
            print("✅ 成功獲取數據！")
            with open("flight_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return True
        else:
            print(f"❌ API 請求失敗，狀態碼: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 連線異常: {e}")
        return False

if __name__ == "__main__":
    check_flights()
