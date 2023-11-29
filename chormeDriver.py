from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from bs4 import BeautifulSoup
from keras.utils import img_to_array
from keras.utils import load_img
from keras.models import load_model
from PIL import Image
from io import BytesIO
import requests
import numpy as np
import cv2
import time
import json
import os


def setup(url,view,path = "m"):
    print("chrome_options setup")
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1280,960")
    if view==False :
        chrome_options.add_argument('--headless')
    if path == "m":
        driver = webdriver.Chrome(options=chrome_options)
    else:
        driver = webdriver.Chrome(executable_path=path, options=chrome_options)
    driver.get(url)
    print("chrome_options ready\n")
    return driver

def switch_frame(reset, frame, driver):
    if reset:
        driver.switch_to.default_content()
    for frame_name in frame:
        right_frame = driver.find_element(By.NAME, frame_name)
        driver.switch_to.frame(right_frame)

def reset_frame(driver):
    driver.switch_to.default_content()