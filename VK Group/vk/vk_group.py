from .vk_self import VKSelf
from config import (
	GROUP_ACCESS_TOKEN,
	GROUP_ID,
)


class VKGroup(VKSelf):
	def __init__(self):
		super().__init__()