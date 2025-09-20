# compare.py
from vision import extract_price_info

def compare_prices(blinkit_img: str, amazon_img: str):
    print("\n🔍 Reading data from Blinkit...")
    blinkit_result = extract_price_info(blinkit_img, "Blinkit")
    print("🟢 Blinkit:", blinkit_result)

    print("\n🔍 Reading data from Amazon...")
    amazon_result = extract_price_info(amazon_img, "Amazon Fresh")
    print("🟢 Amazon Fresh:", amazon_result)

    # Simple price extraction (assumes format: "Name - ₹Price")
    import re

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

    print("\n📊 Your Optimized Product:")
    if blinkit_price < amazon_price:
        print(f"✅ Cheaper on Blinkit: ₹{blinkit_price}")
    elif amazon_price < blinkit_price:
        print(f"✅ Cheaper on Amazon Fresh: ₹{amazon_price}")
    elif blinkit_price == amazon_price and blinkit_price != float("inf"):
        print(f"✅ Same price on both: ₹{blinkit_price}")
    else:
        print("❌ Could not extract valid prices from both images.")
