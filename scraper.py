import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin


base_url = "https://books.toscrape.com/"
books_data = []

# Load old data for incremental scraping
try:
    old_df = pd.read_csv("books.csv")
    old_urls = set(old_df["product_url"])
    print("Existing books:", len(old_df))

except FileNotFoundError:
    old_df = pd.DataFrame()
    old_urls = set()
    print("First run")


rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}


# Scrape all catalogue pages
for page in range(1, 51):

    if page == 1:
        url = base_url
    else:
        url = base_url + f"catalogue/page-{page}.html"

    print("Scraping page:", page)

    response = requests.get(url)

    if response.status_code != 200:
        print("Page failed:", response.status_code)
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")

    if not books:
        break

    for book in books:

        title = book.h3.a["title"]

        product_url = urljoin(
        url,
        book.h3.a["href"]
        )

        # Skip books that were already scraped
        if product_url in old_urls:
            print("Skipping:", title)
            continue

        print("New book:", title)

        # Price
        price = book.find(
            "p",
            class_="price_color"
        ).text.strip()

        price = float(
            price.replace("Â£", "").replace("£", "")
        )

        # Availability
        availability = book.find(
            "p",
            class_="instock availability"
        ).text.strip()

        # Rating
        rating_name = book.find(
            "p",
            class_="star-rating"
        )["class"][1]

        rating = rating_map[rating_name]

        # Image URL
        image_url = urljoin(
            url,
            book.find("img")["src"]
        )

        # Open product page
        product_response = requests.get(product_url)

        if product_response.status_code != 200:
            print("Product page failed:", product_url)
            continue

        product_soup = BeautifulSoup(
            product_response.text,
            "html.parser"
        )

        # Category
        breadcrumb = product_soup.find(
            "ul",
            class_="breadcrumb"
        )

        if breadcrumb:
            items = breadcrumb.find_all("li")
            category = items[-2].text.strip()
        else:
            category = "Unknown"

        # Stock quantity
        stock = product_soup.find(
            "p",
            class_="instock availability"
        )

        stock_quantity = None

        if stock:
            stock_text = stock.text.strip()

            if "(" in stock_text:
                try:
                    stock_quantity = int(
                        stock_text.split("(")[1].split()[0]
                    )
                except (ValueError, IndexError):
                    stock_quantity = None

        books_data.append({
            "title": title,
            "price": price,
            "availability": availability,
            "stock_quantity": stock_quantity,
            "rating": rating,
            "category": category,
            "product_url": product_url,
            "image_url": image_url
        })


# Convert new books to DataFrame
new_df = pd.DataFrame(books_data)

# Combine old and new data
if not old_df.empty:
    final_df = pd.concat(
        [old_df, new_df],
        ignore_index=True
    )
else:
    final_df = new_df

# Remove duplicates
final_df = final_df.drop_duplicates(
    "product_url"
)

# Save output
final_df.to_csv(
    "books.csv",
    index=False
)

print("\nScraping completed")
print("New books:", len(new_df))
print("Total books:", len(final_df))
print("Output: books.csv")