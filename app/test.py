"""
Basic tests of backend features.
"""
import requests

print(requests.post(url = 'https://e7b5-64-201-255-34.ngrok.io/quote', json = {
    "ticker": "NVDA",
    "timeframe": "1mo",
}))

response = requests.post(url = "https://e7b5-64-201-255-34.ngrok.io/macdModel", json = {
    "period":"1mo",
    "interval":"1d",
    "slow":"26",
    "fast":"12",
    "signal":"9"
})

print(response.json())

