"""
Basic tests of backend features.
"""
import requests

print(requests.post(url = 'https://84cc-73-202-118-76.ngrok.io/quote', json = {
    "ticker": "NVDA",
    "timeframe": "1mo",
}))

response = requests.post(url = "https://84cc-73-202-118-76.ngrok.io/macdModel", json = {
    "period":"5d",
    "interval":"1m",
    "slow":"26",
    "fast":"12",
    "signal":"9",
    "shares":"20",
    "starting_price":"160",
    "cash":"1000",
})

print(response.json()["returns"])