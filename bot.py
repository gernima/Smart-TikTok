import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager as CM



class Bot:
    def __init__(self):
        print('=====================================================================================================')
        print('Heyy, you have to login manully on tiktok, so the bot will wait you 1 minute for loging in manually!')
        print('=====================================================================================================')
        time.sleep(8)
        print('Running bot now, get ready and login manually...')
        time.sleep(4)

        options = webdriver.ChromeOptions()
        self.bot = webdriver.Chrome(options=options,  executable_path=CM().install())
        self.bot.set_window_size(1680, 900)

        self.bot.get('https://www.tiktok.com/login')
        ActionChains(self.bot).key_down(Keys.CONTROL).send_keys(
            '-').key_up(Keys.CONTROL).perform()
        ActionChains(self.bot).key_down(Keys.CONTROL).send_keys(
            '-').key_up(Keys.CONTROL).perform()
        print('Waiting 50s for manual login...')
        time.sleep(50)
        self.bot.get('https://www.tiktok.com/upload/?lang=en')
        time.sleep(3)

        # ================================================================
        # Here is the path of the video that you want to upload in tiktok.
        # Plese edit the path because this is different to everyone.
        # upload(r"C:/Users/redi/Videos/your-video-here.mov")


    def check_exists_by_xpath(self, xpath):
        try:
            driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False

        return True


    def upload(self, video_path: string, tags: list):
        file_uploader = self.bot.find_element_by_xpath(
            '//*[@id="main"]/div[2]/div/div[2]/div[2]/div/div/input')

        file_uploader.send_keys(video_path)

        caption = self.bot.find_element_by_xpath(
            '//*[@id="main"]/div[2]/div/div[2]/div[3]/div[1]/div[1]/div[2]/div/div[1]/div/div/div/div/div/div/span')

        self.bot.implicitly_wait(10)
        ActionChains(self.bot).move_to_element(caption).click(
            caption).perform()
        # ActionChains(self.bot).key_down(Keys.CONTROL).send_keys(
        #     'v').key_up(Keys.CONTROL).perform()

        for tag in tags:
            ActionChains(self.bot).send_keys(tag).perform()
            time.sleep(2)
            ActionChains(self.bot).send_keys(Keys.RETURN).perform()
            time.sleep(1)

        time.sleep(5)
        self.bot.execute_script("window.scrollTo(150, 300);")
        time.sleep(5)

        post = WebDriverWait(self.bot, 100).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="main"]/div[2]/div/div[2]/div[3]/div[5]/button[2]')))

        post.click()
        time.sleep(30)

        if check_exists_by_xpath(self.bot, '//*[@id="portal-container"]/div/div/div[1]/div[2]'):
            reupload = WebDriverWait(self.bot, 100).until(EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="portal-container"]/div/div/div[1]/div[2]')))

            reupload.click()
        else:
            print('Unknown error cooldown')
            while True:
                time.sleep(600)
                post.click()
                time.sleep(15)
                if check_exists_by_xpath(self.bot, '//*[@id="portal-container"]/div/div/div[1]/div[2]'):
                    break

        if check_exists_by_xpath(self.bot, '//*[@id="portal-container"]/div/div/div[1]/div[2]'):
            reupload = WebDriverWait(self.bot, 100).until(EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="portal-container"]/div/div/div[1]/div[2]')))
            reupload.click()

        time.sleep(1)

