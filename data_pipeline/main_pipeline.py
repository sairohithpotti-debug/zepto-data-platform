
import re
import urllib.parse
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"

# List of target category relative URLs (picks 3 distinct categories)
CATEGORY_URLS = [
    "catalogue/category/books/travel_2/index.html",
    "catalogue/category/books/mystery_3/index.html",
    "catalogue/category/books/historical-fiction_4/index.html",
]


def scrape_category(category_relative_url):
    books_data = []
    current_url = urllib.parse.urljoin(BASE_URL, category_relative_url)

    while current_url:
        response = requests.get(current_url)
        if response.status_code != 200:
            print(f"Failed to fetch {current_url}")
            break

        soup = BeautifulSoup(response.content, "html.parser")

        # Get category name
        category_name = soup.find("h1").get_text(strip=True)

        # Find all book items on the current page
        articles = soup.find_all("article", class_="product_pod")

        for article in articles:
            # 1. Title
            title = article.h3.a["title"]

            # 2. Price (raw string e.g., '£51.77')
            price_text = article.find("p", class_="price_color").get_text(
                strip=True
            )

            # 3. Star Rating (extract class name e.g., 'star-rating Three' -> 'Three')
            rating_classes = article.find("p", class_="star-rating")["class"]
            rating_text = [c for c in rating_classes if c != "star-rating"][0]

            # 4. Availability (e.g., 'In stock')
            availability_text = article.find(
                "p", class_="instock availability"
            ).get_text(strip=True)

            books_data.append(
                {
                    "title": title,
                    "price": price_text,
                    "star_rating": rating_text,
                    "availability": availability_text,
                    "category": category_name,
                }
            )

        # Pagination check: look for 'next' button
        next_button = soup.find("li", class_="next")
        if next_button:
            next_page_rel = next_button.a["href"]
            current_url = urllib.parse.urljoin(current_url, next_page_rel)
        else:
            current_url = None

    return books_data


def run_scraper():
    all_books = []
    for cat_url in CATEGORY_URLS:
        print(f"Scraping category path: {cat_url}")
        cat_books = scrape_category(cat_url)
        all_books.extend(cat_books)

    print(f"\nSuccessfully scraped {len(all_books)} books total.")
    return all_books


if __name__ == "__main__":
    scraped_data = run_scraper()

    # Preview first scraped entry
    if scraped_data:
        print("\nSample Scraped Record:")
        print(scraped_data[0])

#cleaning code
import pandas as pd
import numpy as np

# Rating text-to-integer mapping dictionary
RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

# Fixed project conversion rate: 1 GBP = 105.50 INR
GBP_TO_INR_RATE = 105.50

def clean_scraped_data(raw_data):
    # Convert list of dicts to a pandas DataFrame
    df = pd.DataFrame(raw_data)

    # -------------------------------------------------------------
    # 1. Clean Price Column (price_gbp)
    # -------------------------------------------------------------
    # Strip currency symbols (e.g., '£', 'Â') and non-numeric characters except '.'
    df['price_gbp'] = df['price'].astype(str).str.replace(r'[^\d.]', '', regex=True)
    # Convert to numeric float (errors='coerce' turns bad parses into NaN)
    df['price_gbp'] = pd.to_numeric(df['price_gbp'], errors='coerce')

    # Handle missing/corrupted prices using median imputation
    if df['price_gbp'].isnull().any():
        median_price = df['price_gbp'].median()
        df['price_gbp'] = df['price_gbp'].fillna(median_price)
        print(f"Imputed missing price_gbp values with median: {median_price}")

    # -------------------------------------------------------------
    # 2. Clean Star Rating Column (rating)
    # -------------------------------------------------------------
    # Map text rating ('Three') to integer (3)
    df['rating'] = df['star_rating'].map(RATING_MAP)
    # Convert to numeric integer type (handle missing with median if any)
    if df['rating'].isnull().any():
        median_rating = df['rating'].median()
        df['rating'] = df['rating'].fillna(median_rating)
    df['rating'] = df['rating'].astype(int)

    # -------------------------------------------------------------
    # 3. Clean Availability Column (in_stock)
    # -------------------------------------------------------------
    # Parse text into boolean (True if 'In stock' is in the text, else False)
    df['in_stock'] = df['availability'].astype(str).str.contains('In stock', case=False, regex=False)

    # -------------------------------------------------------------
    # 4. Currency Conversion (price_inr)
    # -------------------------------------------------------------
    # Compute price_inr using the project's fixed baseline rate
    df['price_inr'] = (df['price_gbp'] * GBP_TO_INR_RATE).round(2)

    # -------------------------------------------------------------
    # 5. Drop Raw Columns & Reorder Final Fields
    # -------------------------------------------------------------
    final_df = df[['title', 'category', 'price_gbp', 'price_inr', 'rating', 'in_stock']].copy()

    return final_df


if __name__ == "__main__":
    # Assuming 'scraped_data' is the output from Step 1
    # Example placeholder raw data for testing:
    sample_raw_data = [
        {"title": "A Light in the Attic", "price": "£51.77", "star_rating": "Three", "availability": "In stock", "category": "Poetry"},
        {"title": "Tipping the Velvet", "price": "£53.74", "star_rating": "One", "availability": "In stock", "category": "Sequential Art"},
        {"title": "Soumission", "price": "£50.10", "star_rating": "One", "availability": "In stock", "category": "Fiction"}
    ]

    cleaned_df = clean_scraped_data(scraped_data)

    print("\n--- Cleaned DataFrame Output ---")
    print(cleaned_df.info())
    print("\nFirst 3 Rows:")
    print(cleaned_df.head())

    # sqlite3 loader code

    def load_df_to_sqlite(cleaned_df, db_name="zepto_books.db"):
    # Connect with a long timeout (60 seconds)
    conn = sqlite3.connect(db_name, timeout=60)
    cursor = conn.cursor()

    try:
        # Enable WAL mode to prevent locking issues & turn on foreign keys
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("PRAGMA foreign_keys = ON;")

        # Create Schema
        cursor.executescript(
            """
            DROP TABLE IF EXISTS books;
            DROP TABLE IF EXISTS categories;

            CREATE TABLE categories (
                category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_name TEXT UNIQUE NOT NULL
            );

            CREATE TABLE books (
                book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                price_gbp REAL NOT NULL,
                price_inr REAL NOT NULL,
                rating INTEGER NOT NULL,
                in_stock INTEGER NOT NULL,
                category_id INTEGER,
                FOREIGN KEY (category_id) REFERENCES categories(category_id)
            );
        """
        )

        # 1. Insert Categories
        categories_df = (
            pd.DataFrame(
                cleaned_df["category"].unique(), columns=["category_name"]
            )
            .reset_index(drop=True)
        )
        categories_df.to_sql(
            "categories", conn, if_exists="append", index=False
        )

        # 2. Map Category IDs
        db_categories = pd.read_sql(
            "SELECT category_id, category_name FROM categories", conn
        )
        full_df = cleaned_df.merge(
            db_categories, left_on="category", right_on="category_name"
        )

        # 3. Format & Insert Books
        books_df = full_df[
            [
                "title",
                "price_gbp",
                "price_inr",
                "rating",
                "in_stock",
                "category_id",
            ]
        ].copy()
        books_df["in_stock"] = books_df["in_stock"].astype(int)

        books_df.to_sql("books", conn, if_exists="append", index=False)

        # Explicitly commit changes
        conn.commit()
        print("Data successfully committed to SQLite!")

    finally:
        # Explicitly close the connection so the lock is released
        conn.close()

# Call the function with the cleaned data
if __name__ == "__main__":
    load_df_to_sqlite(cleaned_df)
