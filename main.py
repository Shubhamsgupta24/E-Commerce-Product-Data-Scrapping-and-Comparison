import streamlit as st
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent

url = "https://www.flipkart.com/search?q=iphone&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
DRIVER_PATH = r"/home/sgubuntu/Projects/Website_Differer/chromedriver-linux64/chromedriver"

    # Initialize Chrome WebDriver options
chrome_options = Options()
chrome_options.binary_location = "/usr/bin/google-chrome-stable"

    # Set Chrome WebDriver executable path
chrome_options.add_argument("webdriver.chrome.driver=" + DRIVER_PATH)

    # Set Chrome WebDriver to run in headless mode if you do not want the popup
    # chrome_options.add_argument("--headless")

    # Exclude the "enable-automation" switch to prevent WebDriver detection
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])

    # Initialize the Chrome WebDriver with the specified options
driver = webdriver.Chrome(options=chrome_options)

    # Open the URL
driver.get(url)
    
    # Get the page source
page_source = driver.page_source

    # Create a BeautifulSoup object to parse the page source
soup = BeautifulSoup(page_source, 'lxml')

    # Close the WebDriver to release resources
driver.quit()

print(soup)
