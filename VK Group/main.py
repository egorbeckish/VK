import requests
import json


access_token = "vk1.a.sIssxfskSOBbbIDN4vJuqOeFIWLULSuN5z1f9i61tiwcgZxc5-ao3LAW56hRaNDP71eAhqk01CtZMfLQEzShdu3Mc2BlrgD9lu766L21K-OZipSYKK8qZinx18PymxqIvVWVhTy0-6nmagaf3koQxiTUs4OydZZG_Qu7O2hxmSRQX-n3-XgLRBjejs-C55D67m_ap-MW2YfRIsdPrkhSrQ"

response = requests.post(
	url="https://api.vk.ru/method/photos.getMessagesUploadServer",
	data={
		"access_token": access_token,
		"peer_id": 388416394,
		"v": 5.199
	}
)

upload_url = response.json()["response"]["upload_url"]

response = requests.post(
	url=upload_url,
	files={
		"photo": open(r"D:\Self Project\Подсчет заданий\ОС\images.png", "rb")
	}
)

response = response.json()
photo = response["photo"]
server = response["server"]
hash = response["hash"]

response = requests.post(
	url="https://api.vk.ru/method/photos.saveMessagesPhoto",
	data={
		"access_token": access_token,
		"photo": photo,
		"server": server,
		"hash": hash,
		"v": 5.199
	}
)

print(response.json())
response = response.json()["response"][0]
owner_id = response["owner_id"]
photo_id = response["id"]

response = requests.post(
	url="https://api.vk.ru/method/messages.send",
	data={
		"access_token": access_token,
		"attachment": f"photo{owner_id}_{photo_id}",
		"user_id": 388416394,
		"random_id": 0,
		"v": 5.199
	}
)