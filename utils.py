import httpx
import numpy as np

EXCLUDED_COINS = ['BTC', 'ETH', 'BNB', 'SOL']

async def calculate_rsi(symbol, interval="1h", limit=100):
    url = f"https://api.mexc.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url)
            data = resp.json()
            closes = [float(entry[4]) for entry in data]
            if len(closes) < 14:
                return None
            deltas = np.diff(closes)
            seed = deltas[:14]
            up = seed[seed > 0].sum() / 14
            down = -seed[seed < 0].sum() / 14
            rs = up / down if down != 0 else 0
            rsi = 100 - 100 / (1 + rs)
            return round(rsi, 2)
        except Exception:
            return None

async def get_filtered_coins():
    coins = []
    url = "https://api.mexc.com/api/v3/ticker/24hr"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        for coin in data:
            symbol = coin['symbol']
            if not symbol.endswith("USDT") or any(ex in symbol for ex in EXCLUDED_COINS):
                continue
            try:
                price = float(coin['lastPrice'])
                volume = float(coin['quoteVolume'])
                change = float(coin['priceChangePercent'])
                if 0.000001 < price < 10 and volume > 500_000 and abs(change) > 10:
                    rsi = await calculate_rsi(symbol)
                    if rsi is not None and 20 < rsi < 70:
                        coins.append({
                            "symbol": symbol,
                            "price": price,
                            "volume": volume,
                            "change": change,
                            "rsi": rsi,
                            "target": round(price * 1.2, 6),
                            "stop_loss": round(price * 0.9, 6),
                        })
            except:
                continue
    return coins
