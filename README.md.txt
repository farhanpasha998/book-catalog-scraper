# Book Catalog Scraper

## Objective

This project scrapes book information from Books to Scrape and stores the data in a CSV file.

## Data Collected

The scraper collects the following fields:

- Title
- Price
- Availability
- Stock Quantity
- Rating
- Category
- Product URL
- Image URL

## Approach

The scraper uses Python Requests to send requests to the website and BeautifulSoup to extract the required information from the HTML pages.

The scraper goes through all catalogue pages. For each new book, it opens the product page to extract the category and stock quantity.

## Data Normalization

- Price is converted into a numeric value.
- Rating is converted from words such as One, Two, Three, Four and Five into integers from 1 to 5.
- Stock quantity is extracted as an integer where available.
- Duplicate records are removed using the product URL.

## Incremental Scraping

The product URL is used as the unique identifier for each book.

Before processing a product page, the scraper checks whether the product URL already exists in books.csv.

If the URL already exists, the book is skipped.

If the URL is new, the product page is processed and the book is added to the output.

This avoids processing unchanged books during later runs.

## Output

The scraper generates:

books.csv

The CSV contains:

- title
- price
- availability
- stock_quantity
- rating
- category
- product_url
- image_url

## How to Run

Install the required packages:

pip install requests beautifulsoup4 pandas

Run the scraper:

python scraper.py

The output will be saved as:

books.csv

## Assumptions

- Product URL is treated as the unique identifier for a book.
- The website structure is assumed to remain consistent while scraping.
- Existing books are skipped during later runs.
- Stock quantity can be empty when it is not available.