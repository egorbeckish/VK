from config import *


VK_ENV = dotenv_values(".env/.env.vk")
GROUP_ACCESS_TOKEN = VK_ENV["GROUP_ACCESS_TOKEN"]
GROUP_ID = VK_ENV["GROUP_ID"]