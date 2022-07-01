"""
Basic tests of backend features.
"""
import requests

# print(requests.post(url = 'https://cae5-73-202-118-76.ngrok.io/quote', json = {
#     "ticker": "TSLA",
#     "timeframe": "1mo",
# }))

# response = requests.post(url = "https://cae5-73-202-118-76.ngrok.io/macdModel", json = {
#     "period":"5d",
#     "interval":"1h",
#     "slow":"26",
#     "fast":"12",
#     "signal":"9",
#     "shares":"1",
#     "starting_price":"700",
#     "cash":"5000",
# })

# print(response.json()["returns"])

response = requests.post(url = "https://cae5-73-202-118-76.ngrok.io/rsiModel", json = {
    "period":"1mo",
    "interval":"1h",
    "window":"5",
    "shares":"1",
    "starting_price":"700",
    "cash":"5000",
})

print(response.json()["returns"])

