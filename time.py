api = "82cfd343470846438bc7522eacfefae1"
import requests


response = requests.get('https://timezone.abstractapi.com/v1/current_time/?api_key={0}&location={1}'.format(api,'nocity'))


data = response.json()
if (str(data) =="{}" ):
    print("empty")
elif data["is_dst"]==False:
    print("Not set")
else:
    print(data)
# print(data["datetime"])
# print(data["datetime"][11:13])
#
# tag = int(data["datetime"][11:13])
# if True:
#                 if tag<=12:
#                     print("day")
#                 elif tag<=18:
#                     print("evening-morning")
#                 elif tag<=23:
#                     print("night")
