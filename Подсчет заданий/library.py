from selenium import webdriver
from selenium.webdriver.edge.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import pandas as pd
import numpy as np
from datetime import datetime
import time
import re
import os
import openpyxl
from dotenv import dotenv_values

LOGIN, PASSWORD, EGE, OGE = dotenv_values(r".env").values()
EGE = int(EGE)
OGE = int(OGE)