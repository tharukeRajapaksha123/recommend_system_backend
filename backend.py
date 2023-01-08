import sqlite3
from fastapi import FastAPI
import uvicorn
import warnings
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from predict_restaurant import PredictRestaurant
from resuturent_finder import RestaurantFinder
from reviews_scraper import ReviewScraper

# initilise api instance
app = FastAPI()

# add cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",
        "http://localhost",
        "http://localhost:3000"
    ],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

warnings.simplefilter("ignore")


# test api endpoint
@app.get("/")
async def read_item():
    return {"message": "api working"}


# get resturents endpoint
@app.get("/{place_name}")
def search_place(place_name: str):
    # debug print
    print(f"search place called {place_name}")
    try:
        # checking whether search location is previously searched
        # if yes it will get data from database and send to user,
        # else it will scrape data from google maps
        with sqlite3.connect("app.db") as conn:
            cursor = conn.cursor()
            results = cursor.execute(f"SELECT * FROM restaurants WHERE city = '{place_name}'")
            restaurants = []

            for row in results:
                data = {
                    "restaurant_name": row[0],
                    "restaurant_link": row[1],
                    "image": row[2]
                }
                restaurants.append(data)
            if len(restaurants) > 0:
                return {"result": restaurants}
            else:
                #start scraping
                review_scraper = ReviewScraper()
                restaurant_finder = RestaurantFinder()
                restaurants = restaurant_finder.finder(place_name)
                restaurant_name_list = []
                restaurant_url_list = []
                restaurant_image_list = []
                restaurant_predict_value_list = []
                print("/n")
                print("restaurant fetching successfully executed ", len(restaurants))
                print("/n")
                counter = 0
                for restaurant in restaurants:
                    reviews_data_set = review_scraper.scraper(restaurant)
                    if reviews_data_set is not None:
                        predict_restaurant = PredictRestaurant()
                        predict_value = predict_restaurant.predictRestaurent(reviews_data_set["duration"])
                        if predict_value != 0.0:
                            print(f"predict value {predict_value} {reviews_data_set.at[0, 'restaurant_name']}")
                            restaurant_name_list.append(reviews_data_set.at[0, 'restaurant_name'])
                            restaurant_url_list.append(reviews_data_set.at[0, 'restaurant_link'])
                            restaurant_predict_value_list.append(predict_value)
                            restaurant_image_list.append(reviews_data_set.at[0, 'image'])
                    print(f"restaurant review predicting for restaurant {counter} done")
                    counter += 1

            df = pd.DataFrame(
                {"restaurant_name": restaurant_name_list,
                 "restaurant_link": restaurant_url_list,
                 "image": restaurant_image_list,
                 'predict_value': restaurant_predict_value_list})

            print(df.nlargest(3, ['predict_value']).head())
            result = df.nlargest(3, ['predict_value']).head()
            response = []
            for index, row in result.iterrows():
                name = row["restaurant_name"]
                address = row["restaurant_link"]
                phone_number = row["image"]
                data = {
                    "restaurant_name": row["restaurant_name"],
                    "restaurant_link": row["restaurant_link"],
                    "image": row["image"],
                    "predict_value": row["predict_value"]
                }
                # insert scraped data into database
                cursor.execute(
                    f"INSERT INTO restaurants VALUES  ('{name}','{address}','{phone_number}','{place_name}')")
                conn.commit()
                response.append(data)
            if not result.empty:
                return {"result": response}
            return {"result": []}
    except Exception as e:
        print("get place failed ", e)
        return {"message": "error"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
