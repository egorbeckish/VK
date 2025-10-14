from selenium import webdriver
from selenium.webdriver.edge.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import time
from datetime import datetime
import re
import pandas as pd
import os
import openpyxl
from dotenv import dotenv_values

LOGIN, PASSWORD = dotenv_values(r".env").values()