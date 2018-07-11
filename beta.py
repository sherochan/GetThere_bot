import django
import requests

r = requests.get('https://api.telegram.org/bot574534905:AAH_w1xrggnjS3fe5yEs6fDf_HXFVJokidQ/getMe')
print(r.text)