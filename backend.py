from fastapi import FastAPI
import uvicorn

from resuturent_finder import RestaurantFinder
from reviews_scraper import ReviewScraper

app = FastAPI()


@app.get("/")
async def read_item():
    return {"message": "api working"}


@app.get("/{place_name}")
def search_place(place_name: str):
    print("called")
    review_scraper = ReviewScraper()
    restaurant_finder = RestaurantFinder()
    restaurants = restaurant_finder.finder(place_name)
    for restaurant in restaurants:
        review_scraper.scraper(restaurant)
        break

    return {"hello": "world"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, timeout_keep_alive=50000)
