from utils import *

class VK:

	def __init__(self) -> None:
		self.__access_token: str = get_token()
		self.__version: str = '5.81'
		self.__url: str = 'https://api.vk.com/method/'
		self.__params: dict[str: int | str] = {
			'access_token': self.__access_token,
			'v': self.__version,
		}
		self.__id = self.self_id
	
	@property
	def self_id(self) -> None:
		response = requests.post(
			url=self.__url + 'account.getProfileInfo',
			params=self.__params
		)
		
		return response.json()['response']['id']
	
	@property
	def access_token(self) -> str:
		return self.__access_token

	@property
	def version(self) -> tuple[int, list[list[str]]]:
		return self.__version
	
	@property
	def get_video(self) -> None:
		response = requests.post(
			url=self.__url + 'video.get',
			params=self.__params
		)

		answer: dict = response.json()['response']
		count_video: int = answer['count']
		videos: list[dict] = answer['items']
		
		return count_video, [
								[
									video['title'], 
									video['player']
								]
								for video in videos
							]
	
	@property
	def get_music(self) -> None:
		response = requests.post(
			url=self.__url + 'audio.get',
			params=self.__params
		)

		return response.json()