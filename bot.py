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
from video import *
import re
from collections import Counter
import pickle


class Bot:
    def __init__(self):
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=options,  executable_path=CM().install())
        self.driver.set_window_size(1366, 768)

        self.driver.get('https://www.tiktok.com/login')
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys(
            '-').key_up(Keys.CONTROL).perform()
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys(
            '-').key_up(Keys.CONTROL).perform()
        if os.path.isfile('cookies.txt'):
            self.load_cookie()
        else:
            print("please login, wait 30 seconds")
            time.sleep(30)
            self.save_cookie()
        time.sleep(3)
        self.t = 180
        self.n = 2
        self.generate_time()

        self.source = os.path.abspath("Videos/101dalmatinec/101dalmatinec.avi").replace("\\", "/")

        self.tags = ["далматинцы", "мультик", "дисней", "момент", "нарезка", "101", "disney", "waltdisney", "анимация", "собаки", "animation"]
        with open("popular_tags.txt", "r") as f:
            for i in f.read().split():
                self.tags.append(i.replace("#", ""))
        self.description = ""
        self.thread_name = "thread_1"
        # ================================================================
        # Here is the path of the video that you want to upload in tiktok.
        # Plese edit the path because this is different to everyone.
        # upload(r"C:/Users/redi/Videos/your-video-here.mov")

    def generate_time(self):
        self.t1 = self.n * self.t
        self.t2 = (self.n + 1) * self.t

    def save_cookie(self):
        pickle.dump(self.driver.get_cookies() , open("cookies.txt","wb"))

    def load_cookie(self):
        cookies = pickle.load(open("cookies.txt", "rb"))
        for cookie in cookies:
            self.driver.add_cookie(cookie)

    # def generate_tags(self, text):
    #     text = text.lower()
    #     words = re.findall(r'\w+', text)
    #     word_counts = sorted(Counter(words), key=lambda x: len(x) >= )
    #     i = 0
    #     while len("#".join(self.tags)) <= (150 - len(self.description)):

    def check_exists_by_xpath(self, xpath):
        try:
            self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False

        return True

    def upload(self):
        self.driver.get('https://www.tiktok.com/upload/?lang=en')
        time.sleep(5)
        file_uploader = self.driver.find_element_by_xpath(
            '//*[@id="main"]/div[2]/div/div[2]/div[2]/div/div/input')

        create_subclip(self.source, self.t1, self.t2, self.thread_name)

        self.n += 1
        self.generate_time()

        file_uploader.send_keys(os.path.abspath(f"Clips/{self.thread_name}/clip.mp4").replace("\\", "/"))

        caption = self.driver.find_element_by_xpath(
            '//*[@id="main"]/div[2]/div/div[2]/div[3]/div[1]/div[1]/div[2]/div/div[1]/div/div/div/div/div/div/span')

        self.driver.implicitly_wait(10)
        ActionChains(self.driver).move_to_element(caption).click(
            caption).perform()
        # ActionChains(self.driver).key_down(Keys.CONTROL).send_keys(
        #     'v').key_up(Keys.CONTROL).perform()
        # self.generate_tags(video.get_text(video, thread_name))

        ActionChains(self.driver).send_keys(self.description).perform() # write descriprion
        
        for tag in random.sample(self.tags, 10): # write tags
            ActionChains(self.driver).send_keys(" #" + tag).perform()
            time.sleep(3)
            ActionChains(self.driver).send_keys(Keys.RETURN).perform()
            time.sleep(1)

        time.sleep(5)
        self.driver.execute_script("window.scrollTo(150, 300);")
        time.sleep(5)

        post = WebDriverWait(self.driver, 100).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="main"]/div[2]/div/div[2]/div[3]/div[6]/button[2]')))

        post.click()
        # time.sleep(30)
        while self.check_exists_by_xpath('//*[@id="main"]/div[2]/div/div[2]/div[2]/div/div[1]/div[2]'):
            pass
        time.sleep(10)
        self.driver.find_element_by_xpath('//*[@id="main"]/div[2]/div/div[2]/div[3]/div[6]/button[2]').click()
        print(f"{self.thread_name} loaded {self.source.split('/')[-1]} from {self.t1} to {self.t2}")
        with open("ended settings.txt", "a") as f:
            f.write(f"{self.thread_name} loaded {self.source.split('/')[-1]} from {self.t1} to {self.t2}" + "\n")
        # if self.check_exists_by_xpath('//*[@id="portal-container"]/div/div/div[1]/div[2]'):
        #     reupload = WebDriverWait(self.driver, 100).until(EC.visibility_of_element_located(
        #         (By.XPATH, '//*[@id="portal-container"]/div/div/div[1]/div[2]')))

        #     reupload.click()
        # else:
        #     print('Unknown error cooldown')
        #     while True:,
        #         time.sleep(600)
        #         post.click()
        #         time.sleep(15)
        #         if self.check_exists_by_xpath('//*[@id="portal-container"]/div/div/div[1]/div[2]'):
        #             break

        # if self.check_exists_by_xpath('//*[@id="portal-container"]/div/div/div[1]/div[2]'):
        #     reupload = WebDriverWait(self.driver, 100).until(EC.visibility_of_element_located(
        #         (By.XPATH, '//*[@id="portal-container"]/div/div/div[1]/div[2]')))
        #     reupload.click()

        time.sleep(3)

bot = Bot()
while True:
    bot.upload()
