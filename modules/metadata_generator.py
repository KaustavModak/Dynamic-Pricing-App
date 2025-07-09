import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

# --- CONFIG ---
META_PATH = '../data/full_retail_meta_dataset.csv'


def generate_metadata(samples_per_product=1):
    np.random.seed(42)
    today = datetime.today()

    products = [
        {'product_name': 'Fresh Red Apples 1kg', 'category': 'fresh fruits', 'mrp': 120},
        {'product_name': 'Fresh Spinach Bunch', 'category': 'fresh vegetables', 'mrp': 40},
        {'product_name': 'Lays Classic Salted Chips 100g', 'category': 'packaged snacks', 'mrp': 20},
        {'product_name': 'Amul Full Cream Milk 1L', 'category': 'dairy', 'mrp': 65},
        {'product_name': 'Fresho Frozen Sweet Corn 500g', 'category': 'frozen foods', 'mrp': 90},
        {'product_name': 'Tata Tea Gold 250g', 'category': 'beverages', 'mrp': 115},
        {'product_name': 'Nivea Soft Moisturizer 100ml', 'category': 'skincare', 'mrp': 120},
        {'product_name': 'Dove Hair Fall Rescue Shampoo 340ml', 'category': 'haircare', 'mrp': 250},
        {'product_name': 'Dettol Original Bathing Soap 125g', 'category': 'bath & body', 'mrp': 45},
        {'product_name': 'Colgate MaxFresh Toothpaste 150g', 'category': 'oral care', 'mrp': 90},
        {'product_name': 'Stayfree Secure XL 20 pads', 'category': 'sanitary products', 'mrp': 110},
        {'product_name': 'Surf Excel Matic Top Load 2kg', 'category': 'laundry detergents', 'mrp': 370},
        {'product_name': 'Vim Dishwash Gel 500ml', 'category': 'dishwashing liquids', 'mrp': 95},
        {'product_name': 'Lizol Floral Floor Cleaner 1L', 'category': 'floor cleaners', 'mrp': 185},
        {'product_name': 'Odonil Air Freshener Block 50g', 'category': 'air fresheners', 'mrp': 55},
        {'product_name': 'Maggi 2-Minute Noodles 70g', 'category': 'instant noodles', 'mrp': 14},
        {'product_name': 'Fortune Sunflower Oil 1L', 'category': 'cooking oil', 'mrp': 135},
        {'product_name': 'Everest Red Chilli Powder 100g', 'category': 'spices & condiments', 'mrp': 60},
        {'product_name': 'Britannia Whole Wheat Bread 400g', 'category': 'biscuits & breads', 'mrp': 45},
        {'product_name': 'Boat Rockerz Wireless Earbuds', 'category': 'headphones / earbuds', 'mrp': 1899},
        {'product_name': 'MI USB Type-C Charger', 'category': 'mobile accessories', 'mrp': 599},
        {'product_name': 'Zebronics USB Keyboard', 'category': 'computer peripherals', 'mrp': 499},
        {'product_name': 'Wipro Smart Plug 10A', 'category': 'smart devices', 'mrp': 999},
        {'product_name': 'Pampers Baby Dry Diapers M 20pcs', 'category': 'diapers', 'mrp': 449},
        {'product_name': 'Nestle Cerelac Wheat Apple 300g', 'category': 'baby food', 'mrp': 220},
        {'product_name': 'Chicco Soft Toy for Babies', 'category': 'toys', 'mrp': 299},
        {'product_name': 'Himalaya Baby Lotion 100ml', 'category': 'baby lotion & wipes', 'mrp': 125},
        {'product_name': 'Pedigree Adult Dog Food 3kg', 'category': 'dog food', 'mrp': 749},
        {'product_name': 'Drools Cat Litter 5kg', 'category': 'cat litter', 'mrp': 299},
        {'product_name': 'Petzone Squeaky Toy', 'category': 'pet toys', 'mrp': 150},
        {'product_name': 'Himalaya Erina Pet Shampoo 200ml', 'category': 'pet shampoo', 'mrp': 165},
        {'product_name': 'Prestige Non-stick Fry Pan 240mm', 'category': 'non-stick cookware', 'mrp': 799},
        {'product_name': 'Milton Airtight Storage Jar Set', 'category': 'storage jars', 'mrp': 499},
        {'product_name': 'Borosil Glass Lunch Box Set', 'category': 'lunch boxes', 'mrp': 899},
        {'product_name': 'Cello Stainless Steel Bottle 1L', 'category': 'water bottles', 'mrp': 450},
        {'product_name': 'Classmate Notebook 200 pages', 'category': 'notebooks', 'mrp': 40},
        {'product_name': 'Reynolds Trimax Gel Pen Pack of 3', 'category': 'pens & markers', 'mrp': 60},
        {'product_name': 'AmazonBasics Desk Organizer', 'category': 'desk organizers', 'mrp': 350},
        {'product_name': 'JK Copier Paper A4 500 Sheets', 'category': 'printer paper', 'mrp': 280},
        {'product_name': 'Bombay Dyeing Double Bedsheet', 'category': 'bedsheets', 'mrp': 899},
        {'product_name': 'Trident Bath Towels Set of 2', 'category': 'towels', 'mrp': 499},
        {'product_name': 'Window Curtain Pair 7ft', 'category': 'curtains', 'mrp': 1099},
        {'product_name': 'LED String Fairy Lights 10m', 'category': 'home decor', 'mrp': 399},
        {'product_name': 'Revital H Multivitamins 30 Tabs', 'category': 'multivitamins', 'mrp': 325},
        {'product_name': 'Lifebuoy Total Hand Sanitizer 500ml', 'category': 'sanitizers', 'mrp': 120},
        {'product_name': 'Dr Trust Infrared Thermometer', 'category': 'thermometers', 'mrp': 1499},
        {'product_name': 'Moov Pain Relief Spray 80g', 'category': 'pain relief spray', 'mrp': 180},
        {'product_name': 'Atomic Habits by James Clear', 'category': 'non-fiction books', 'mrp': 499},
        {'product_name': 'RD Sharma Class 10 Math Book', 'category': 'academic texts', 'mrp': 480},
        {'product_name': 'Diwali Gift Hamper Box', 'category': 'gift hampers', 'mrp': 699},
        {'product_name': 'Clay Diyas Pack of 12', 'category': 'diyas / lights', 'mrp': 180},
        {'product_name': 'Holi Organic Color Pack', 'category': 'holi colors', 'mrp': 160},
        {'product_name': 'Christmas Tree Decor Kit', 'category': 'christmas decor', 'mrp': 550}
    ]

    zones = ['Tier-1', 'Tier-2', 'Tier-3']
    states = [
        'Maharashtra', 'Delhi', 'Karnataka', 'Tamil Nadu', 'West Bengal',
        'Gujarat', 'Rajasthan', 'Uttar Pradesh', 'Kerala', 'Telangana'
    ]

    data = []
    for product in products:
        for state in states:
            for zone in zones:
                for _ in range(samples_per_product):
                    mfg_date = today - timedelta(days=np.random.randint(0, 60))
                    shelf_life = np.random.randint(10, 45)
                    exp_date = mfg_date + timedelta(days=shelf_life)
                    inventory = np.random.randint(10, 1000)

                    data.append([
                        product['product_name'],
                        product['category'],
                        product['mrp'],
                        mfg_date.strftime('%Y-%m-%d'),
                        exp_date.strftime('%Y-%m-%d'),
                        zone,
                        state,
                        inventory
                    ])

    df = pd.DataFrame(data, columns=[
        'product_name', 'category', 'mrp',
        'manufacturing_date', 'expiry_date',
        'location_zone', 'state', 'inventory_level'
    ])

    os.makedirs(os.path.dirname(META_PATH), exist_ok=True)
    df.to_csv(META_PATH, index=False)
    print(f"✅ Metadata generated and saved to: {META_PATH}")


if __name__ == '__main__':
    generate_metadata(samples_per_product=1)
