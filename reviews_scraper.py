from selenium import webdriver
import pandas as pd
import time


class ReviewScraper:
    PATH = "./chromedriver.exe"
    chrome_driver_path = PATH

    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)

    SCROLL_PAUSE_TIME = 2

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    name_list = []
    stars_list = []
    review_list = []
    duration_list = []
    restaurant_name_list = []
    restaurant_link_list = []
    restaurant_image_list = []

    def scraper(self, url):
        number = 0
        self.driver.get(url)
        try:
            driver = self.driver.find_element_by_xpath(
                "/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/div[2]/span[2]/span[1]/span")
        except Exception as e:
            print("view reviews button not found")
            return None
        driver.click()

        r_name = "no_name"

        try:
            r_name = self.driver.find_element_by_xpath(
                "/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/h1").text
        except Exception as e:
            print("restaurant name find failed")
            return None

        print(f"scraping reviews from {r_name}")
        r_image = ""
        try:
            image_container = self.driver.find_element_by_class_name(
                "ZKCDEc")
            image = image_container.find_element_by_tag_name("img")

            r_image = image.get_attribute("src")
            print(r_image)
        except Exception as e:
            print("image found failed")

        time.sleep(5)
        while True:
            number = number + 1

            # Scroll down to bottom

            ele = self.driver.find_element_by_xpath('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]')
            self.driver.execute_script('arguments[0].scrollBy(0, 5000);', ele)

            # Wait to load page

            time.sleep(self.SCROLL_PAUSE_TIME)

            ele = self.driver.find_element_by_xpath('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]')

            new_height = self.driver.execute_script("return arguments[0].scrollHeight", ele)

            if number == 4:
                break

            if new_height == self.last_height:
                break

            self.last_height = new_height
            try:
                item = self.driver.find_elements_by_xpath(
                    '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[9]')
                time.sleep(5)
                for i in item:
                    button = i.find_elements_by_tag_name('button')
                    for m in button:
                        if m.text == "More":
                            m.click()
                    time.sleep(2)
                    duration = i.find_elements_by_class_name("rsqaWe")
                    if duration == "":
                        continue
                    name = i.find_elements_by_class_name("d4r55")
                    stars = i.find_elements_by_class_name("kvMYJc")
                    review = i.find_elements_by_class_name("wiI7pd")

                    for j, k, l, p in zip(name, stars, review, duration):
                        #print(l.text)
                        #print(len(l.text))
                        self.restaurant_name_list.append(r_name)
                        self.restaurant_image_list.append(r_image)
                        self.restaurant_link_list.append(url)
                        self.name_list.append(j.text)
                        self.stars_list.append(p.text)
                        self.review_list.append(k.get_attribute("aria-label"))
                        self.duration_list.append(l.text)
            except Exception as e:
                print(f"item find error {e}")
                pass

        review = pd.DataFrame(
            {"restaurant_name": self.restaurant_name_list,
             "restaurant_link": self.restaurant_link_list,
             "image": self.restaurant_image_list,
             'name': self.name_list,
             'rating': self.stars_list,
             'review': self.review_list,
             'duration': self.duration_list})

        self.restaurant_link_list = []
        self.restaurant_name_list = []
        self.restaurant_image_list = []
        self.name_list = []
        self.stars_list = []
        self.review_list = []
        self.duration_list = []
        return review
