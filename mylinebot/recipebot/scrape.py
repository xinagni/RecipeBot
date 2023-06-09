from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import requests

class Food(ABC):

    def __init__(self, food):
        self.food = food
    
    @abstractmethod
    def scrape(self):
        pass

class Recipe(Food):

    def scrape(self):

        
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        executable_path = 'C:\chromedriver\chromedriver.exe'
        driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)
        driver.get("https://www.ytower.com.tw")

        response = requests.get("https://www.ytower.com.tw/recipe/")
        soup = BeautifulSoup(response.content, "html.parser")

        #處理使用者輸入資訊
        elements = driver.find_element(By.ID, "keyword")
        foodlist = self.food.split(" ")

        elements.send_keys(foodlist[1])
        for i in range(2,len(foodlist)):
            elements.send_keys(" and " + foodlist[i])

        #爬蟲搜索資訊
        elements.send_keys(Keys.ENTER)
        time.sleep(2)

        #爬出每一項食譜名稱
        name = ''
        for i in range(1,6):
            xpath_str = f"//body/div[@id='main']/div[@id='rightmain']/div[2]/div[4]/ul[1]/li[{i}]/a[1]/picture[1]/img[1]"
            item = driver.find_element(By.XPATH, xpath_str)
            driver.execute_script("arguments[0].click();", item)
            time.sleep(2)
                
            soup = BeautifulSoup(driver.page_source, "html.parser")
            div = soup.find('div', {'id': 'recipe_name'})
            h2 = div.find('h2')
            recipe_name = div.find('a').get_text()
            print(recipe_name)
            name += recipe_name+','
            driver.back()
            time.sleep(2)

        time.sleep(5)
        driver.close()

        content=name
        
        return content




