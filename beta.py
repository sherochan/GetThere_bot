import django
import requests

#path = r"C:/Users/toh15/.ssh/test/GetThere_bot_token.txt"
# getting the API token
with open("GetThere_bot_token.txt",'r') as myfile:
    data = myfile.read().replace('\n', '')

print(data)
r = requests.get('https://api.telegram.org/bot574534905:AAH_w1xrggnjS3fe5yEs6fDf_HXFVJokidQ/getMe')
print(r.text)