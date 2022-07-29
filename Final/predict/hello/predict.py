from urllib import response
import requests

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Token ea89232c51f5637589a50f485ccd36f306b18970'
    
}

def get_meta_data(predict):
    url = "https://api.tiingo.com/tiingo/daily/{}".format(predict)
    response = requests.get(url, headers=headers)
    return response.json()

def get_price_data(predict):
    url = "https://api.tiingo.com/tiingo/daily/{}/prices".format(predict)
    response = requests.get(url, headers=headers)
    return response.json()[0]

