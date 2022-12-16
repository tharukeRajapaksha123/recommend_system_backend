import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class RestaurantFinder:
    SCROLL_PAUSE_TIME = 5
    PATH = "./chromedriver.exe"
    chrome_driver_path = PATH

    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    counter = 0

    def finder(self, name):
        link_list = []
        self.counter += 1
        try:
            MAIN_URL = f"https://www.google.com/maps/search/resturents+near+{name}/@51.5140369,-0.1480094,13z/data=!3m1!4b1"
            self.driver.get(MAIN_URL)
            time.sleep(5)
            result_section = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH,
                                                "/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]"))
            )

            while True:
                self.counter += 1
                self.driver.execute_script('arguments[0].scrollBy(0, 5000);', result_section)
                time.sleep(self.SCROLL_PAUSE_TIME)
                result_section = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    "/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]"))
                )
                new_height = self.driver.execute_script("return arguments[0].scrollHeight", result_section)

                if self.counter == 4:
                    break
                if new_height == self.last_height:
                    break

                self.last_height = new_height
                a_tags = result_section.find_elements_by_class_name("hfpxzc")
                time.sleep(5)
                for tag in a_tags:
                    link_list.append(tag.get_attribute('href'))

            link_list = list(dict.fromkeys(link_list))

            return link_list
        except Exception as e:
            print(f"get restaurent links failed {e}")
            pass

        return
