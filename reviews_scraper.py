from selenium import webdriver
import pandas as pd
import time


class ReviewScraper:
    PATH = "./chromedriver.exe"
    chrome_driver_path = PATH

    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)

    SCROLL_PAUSE_TIME = 5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    number = 0
    name_list = []
    stars_list = []
    review_list = []
    duration_list = []
    restaurant_name_list = []
    restaurant_address_list = []
    restaurant_phone_number_list = []

    def scraper(self, url):
        self.driver.get(url)
        driver = self.driver.find_element_by_xpath(
            "/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/div[2]/span[2]/span[1]/span")
        driver.click()

        r_name = self.driver.find_element_by_xpath(
            "/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/h1/span[1]").text
        r_address = self.driver.find_element_by_css_selector(
            "div.RcCsl:nth-child(3) > button:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)").text
        r_phone_number = self.driver.find_element_by_css_selector(
            "div.RcCsl:nth-child(5) > button:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)").text

        time.sleep(5)
        while True:
            self.number = self.number + 1

            # Scroll down to bottom

            ele = self.driver.find_element_by_xpath('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]')
            self.driver.execute_script('arguments[0].scrollBy(0, 5000);', ele)

            # Wait to load page

            time.sleep(self.SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            print(f'last height: {self.last_height}')

            ele = self.driver.find_element_by_xpath('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]')

            new_height = self.driver.execute_script("return arguments[0].scrollHeight", ele)

            print(f'new height: {new_height}')

            if self.number == 2:
                break

            if new_height == self.last_height:
                break

            print('cont')
            self.last_height = new_height
            item = self.driver.find_elements_by_xpath(
                '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[9]')
            time.sleep(5)
            for i in item:
                button = i.find_elements_by_tag_name('button')
                for m in button:
                    if m.text == "More":
                        m.click()
                time.sleep(5)
                name = i.find_elements_by_class_name("d4r55")
                stars = i.find_elements_by_class_name("kvMYJc")
                review = i.find_elements_by_class_name("wiI7pd")
                duration = i.find_elements_by_class_name("rsqaWe")
                for j, k, l, p in zip(name, stars, review, duration):
                    self.restaurant_name_list.append(r_name)
                    self.restaurant_address_list.append(r_address)
                    self.restaurant_phone_number_list.append(r_phone_number)
                    self.name_list.append(j.text)
                    self.stars_list.append(p.text)
                    self.review_list.append(k.get_attribute("aria-label"))
                    self.duration_list.append(l.text)

        review = pd.DataFrame(
            {"restaurant_name": self.restaurant_name_list,
             "phone_number": self.restaurant_phone_number_list,
             "address": self.restaurant_address_list,
             'name': self.name_list,
             'rating': self.stars_list,
             'review': self.review_list,
             'duration': self.duration_list})

        print(review.head())

        return review
