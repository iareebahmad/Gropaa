# browser.py
import webbrowser
import time
import urllib.parse

def open_product_urls(query: str):
    blinkit_url = f"https://blinkit.com/s/?q={query}"
    amazon_url = f"https://www.amazon.in/s?k={query}&rh=p_85%3A10440599031"

    print("\n🌐 Opening product pages in browser...")
    webbrowser.open_new(blinkit_url)
    webbrowser.open_new_tab(amazon_url)
    print("✅ Tabs opened. Please wait for pages to fully load.")

