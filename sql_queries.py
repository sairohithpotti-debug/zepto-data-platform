import sqlite3
import pandas as pd

DB_NAME = "zepto_books.db"


def run_step_4_queries_and_comparisons():
    conn = sqlite3.connect(DB_NAME)

    print("==================================================")
    print("STEP 4: SQL QUERIES & PANDAS REPRODUCTION")
    print("==================================================\n")

    # -------------------------------------------------------------
    # QUERY 1: SELECT / WHERE / ORDER BY / LIMIT
    # Top 5 most expensive books in INR
    # -------------------------------------------------------------
    sql_1 = """
        SELECT title, price_gbp, price_inr, rating 
        FROM books 
        WHERE in_stock = 1 
        ORDER BY price_inr DESC 
        LIMIT 5;
    """
    df_sql_1 = pd.read_sql(sql_1, conn)
    print("--- Query 1: Top 5 Expensive Books In Stock (SQL) ---")
    print(df_sql_1.to_string(index=False))
    print("\n" + "-" * 50 + "\n")

    # -------------------------------------------------------------
    # QUERY 2: DISTINCT
    # List all unique ratings present in the dataset
    # -------------------------------------------------------------
    sql_2 = """
        SELECT DISTINCT rating 
        FROM books 
        ORDER BY rating DESC;
    """
    df_sql_2 = pd.read_sql(sql_2, conn)
    print("--- Query 2: Distinct Star Ratings (SQL) ---")
    print(df_sql_2.to_string(index=False))
    print("\n" + "-" * 50 + "\n")

    # -------------------------------------------------------------
    # QUERY 3: IN / BETWEEN
    # Books with rating between 4 and 5, priced between 20 and 40 GBP
    # -------------------------------------------------------------
    sql_3 = """
        SELECT title, price_gbp, rating 
        FROM books 
        WHERE rating IN (4, 5) 
          AND price_gbp BETWEEN 20.0 AND 40.0
        ORDER BY price_gbp ASC;
    """
    df_sql_3 = pd.read_sql(sql_3, conn)
    print(
        "--- Query 3: Highly Rated Books (4-5) Priced £20-£40 (SQL) ---"
    )
    print(df_sql_3.to_string(index=False))
    print("\n" + "-" * 50 + "\n")

    # -------------------------------------------------------------
    # QUERY 4: JOIN
    # Top 10 highest-rated books with category names
    # -------------------------------------------------------------
    sql_4 = """
        SELECT b.title, c.category_name, b.rating, b.price_inr
        FROM books b
        JOIN categories c ON b.category_id = c.category_id
        ORDER BY b.rating DESC, b.price_inr DESC
        LIMIT 10;
    """
    df_sql_4 = pd.read_sql(sql_4, conn)
    print("--- Query 4: Top 10 Highest Rated Books with Categories (SQL JOIN) ---")
    print(df_sql_4.to_string(index=False))
    print("\n" + "=" * 50 + "\n")

    # -------------------------------------------------------------
    # QUERY 5: AGGREGATION + JOIN (Bonus Clause demonstration)
    # Average price per category
    # -------------------------------------------------------------
    sql_5 = """
        SELECT c.category_name, COUNT(b.book_id) as book_count, ROUND(AVG(b.price_inr), 2) as avg_price_inr
        FROM books b
        JOIN categories c ON b.category_id = c.category_id
        GROUP BY c.category_name;
    """
    df_sql_5 = pd.read_sql(sql_5, conn)
    print("--- Query 5: Average Price by Category (SQL JOIN + GROUP BY) ---")
    print(df_sql_5.to_string(index=False))
    print("\n" + "=" * 50 + "\n")

    # -------------------------------------------------------------
    # PANDAS REPRODUCTION & COMPARISON (Requirement 6)
    # -------------------------------------------------------------
    print("==================================================")
    print("REPRODUCING SQL RESULTS USING PURE PANDAS (NO SQL JOIN)")
    print("==================================================\n")

    # Fetch raw tables without SQL JOIN
    raw_books = pd.read_sql("SELECT * FROM books;", conn)
    raw_categories = pd.read_sql("SELECT * FROM categories;", conn)

    # 1. Reproducing Query 3 in pure Pandas
    pandas_q3 = (
        raw_books[
            (raw_books["rating"].isin([4, 5]))
            & (raw_books["price_gbp"].between(20.0, 40.0))
        ][["title", "price_gbp", "rating"]]
        .sort_values(by="price_gbp", ascending=True)
        .reset_index(drop=True)
    )

    # 2. Reproducing Query 4 (JOIN query) using pure Pandas pd.merge()
    pandas_q4 = (
        pd.merge(
            raw_books, raw_categories, on="category_id", how="inner"
        )
        .sort_values(by=["rating", "price_inr"], ascending=[False, False])[
            ["title", "category_name", "rating", "price_inr"]
        ]
        .head(10)
        .reset_index(drop=True)
    )

    print("--- Pure Pandas Result for Query 4 (pd.merge) ---")
    print(pandas_q4.to_string(index=False))
    print("\n")

    # Match Verification
    sql_join_result = df_sql_4.reset_index(drop=True)
    are_equal = sql_join_result.equals(pandas_q4)

    print(
        f"VERIFICATION: Do SQL JOIN and Pandas pd.merge() outputs match perfectly? -> {are_equal}"
    )

    conn.close()


if __name__ == "__main__":
    run_step_4_queries_and_comparisons()
