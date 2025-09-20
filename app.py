# app.py
import time
import os
from browser import open_product_urls
from capture import take_screenshot
from compare import compare_prices

def main():
    print("🛒 Grocery Optimization Assistant")
    query = input("What's on the list today? ").strip()

    if not query:
        print("❌ Please enter a valid product name.")
        return

    # Open browser tabs for Amazon Fresh and Blinkit
    open_product_urls(query)

    input("\nAfter the pages have fully loaded, press Enter to capture data points...")

    # Take screenshots for reading data points
    input("\nAfter the Blinkit page has fully loaded, press Enter to capture Blinkit ...")
    blinkit_path = take_screenshot("blinkit.png")
    print("✅ Blinkit Scanned")

    input("\nNow switch to the Amazon tab, then press Enter to capture Amazon ...")
    amazon_path = take_screenshot("amazon.png")
    print("✅ Amazon Scanned\n")

    # Wait briefly to ensure files are saved
    time.sleep(1)

    # Compare prices
    compare_prices(blinkit_path, amazon_path)

    # Cleanup the searches
    if os.path.exists(blinkit_path):
        os.remove(blinkit_path)
    if os.path.exists(amazon_path):
        os.remove(amazon_path)

if __name__ == "__main__":
    main()
