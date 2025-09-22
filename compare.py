# compare.py
from vision import extract_price_info
import re

def compare_prices(blinkit_img: str, amazon_img: str):
    # Extract data from Blinkit
    blinkit_result = extract_price_info(blinkit_img, "Blinkit")

    # Extract data from Amazon
    amazon_result = extract_price_info(amazon_img, "Amazon Fresh")

    # Helper to get numeric price
    def get_price(text):
        match = re.search(r"₹\s?([\d,.]+)", text)
        if match:
            price_str = match.group(1).replace(",", "")
            try:
                return float(price_str)
            except:
                return float("inf")
        return float("inf")

    blinkit_price = get_price(blinkit_result)
    amazon_price = get_price(amazon_result)

    # Determine overall lowest
    if blinkit_price < amazon_price:
        overall = f"✅ Cheaper on Blinkit: ₹{blinkit_price}"
    elif amazon_price < blinkit_price:
        overall = f"✅ Cheaper on Amazon Fresh: ₹{amazon_price}"
    elif blinkit_price == amazon_price and blinkit_price != float("inf"):
        overall = f"✅ Same price on both: ₹{blinkit_price}"
    else:
        overall = "❌ Could not extract valid prices from both platforms."

    # Return structured result
    return {
        "blinkit": blinkit_result,
        "amazon": amazon_result,
        "overall": overall
    }
