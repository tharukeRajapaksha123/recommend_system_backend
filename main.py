from resuturent_finder import RestaurantFinder
from reviews_scraper import ReviewScraper


def main():
    review_scraper = ReviewScraper()
    restaurant_finder = RestaurantFinder()
    restaurants = restaurant_finder.finder("bandarawela")
    for restaurant in restaurants:
        review_scraper.scraper(restaurant)
        #print(restaurant)
        break

if __name__ == "__main__":
    main()
