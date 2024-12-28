from utils import *

class VK:

	def __init__(self, token: str) -> None:
		self.__access_token: str = token[token.index('vk1'):token.index('&')]
		self.__version: str = '5.131'
		self.__url: str = 'https://api.vk.com/method/'
		self.__params: dict[str: int | str] = {
			'access_token': self.__access_token,
			'v': self.__version,
		}
		self.__id = self.self_id
	
	@property
	def access_token(self) -> str:
		return self.__access_token

	@property
	def version(self) -> str:
		return self.__version
	
	@property
	def self_id(self) -> int:
		response = requests.post(
			url=self.__url + 'account.getProfileInfo',
			params=self.__params
		)
		
		return response.json()['response']['id']
	
	@property
	def self_fullname(self) -> str:
		response = requests.post(
			url=self.__url + 'account.getProfileInfo',
			params=self.__params
		)
		
		response = response.json()['response']
		return f'{response['first_name']} {response['last_name']}'
	
	def send_message(
			self, 
			user_ids: str,
			message: str,
		) -> None:

		self.__params['message'] = str(message)
		self.__params['random_id'] = 0

		if len(user_ids) > 1:
			self.__params['peer_ids'] = user_ids
		
		else:
			self.__params['peer_id'] = user_ids
		
		responce = requests.post(
			url=f'{self.__url}messages.send',
			params=self.__params
		)

		responce = responce.json()['response']

		error_dict = {
			'ID': [],
			'CODE': [],
			'ERROR': []
		}
		for message in responce:
			if 'error' not in message.keys():
				continue
			
			__id: str = message['peer_id'] 
			error: dict[str: str] = message['error']
			code: str = error['code']
			error_message: str = error['description']

			error_dict['ID'] += [__id]
			error_dict['CODE'] += [code]
			error_dict['ERROR'] += [error_message]
		
		pd.DataFrame(error_dict).to_csv('error_id.csv', index=False)