from library import *

def get_token() -> str:
	access_token = os.environ['VK_TOKEN']
	return access_token[access_token.index('vk1'):access_token.index('&')]