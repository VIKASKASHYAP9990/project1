import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_mock_superstore(filename="superstore.csv", num_rows=1000):
    np.random.seed(42)
    
    # Categories and Sub-categories
    cat_subcat = {
        "Technology": ["Phones", "Accessories", "Copiers", "Machines"],
        "Furniture": ["Chairs", "Tables", "Bookcases", "Furnishings"],
        "Office Supplies": ["Paper", "Binders", "Art", "Appliances", "Envelopes", "Fasteners"]
    }
    
    # Products mapped to sub-categories
    products = {
        "Phones": ["iPhone 15 Pro", "Samsung Galaxy S24", "Google Pixel 8", "OnePlus 12"],
        "Accessories": ["Logitech MX Master 3S", "Keychron K2 Keyboard", "Anker USB-C Hub", "Apple Pencil"],
        "Copiers": ["Canon ImageCLASS", "HP LaserJet Pro Copier", "Brother Monochrome Copier"],
        "Machines": ["Epson EcoTank Pro", "Cricut Maker 3", "3D Printer Ender 3"],
        "Chairs": ["Herman Miller Aeron", "Steelcase Gesture", "Autonomous ErgoChair", "IKEA Markus"],
        "Tables": ["Standing Desk Birch", "Conference Table Mahogany", "Dining Table Oak", "Coffee Table Pine"],
        "Bookcases": ["Billy Bookcase White", "Industrial Metal Bookshelf", "Solid Wood Bookcase"],
        "Furnishings": ["Desk Lamp LED", "Floor Rug Geometric", "Wall Clock Modern", "Picture Frame Set"],
        "Paper": ["Premium Copy Paper A4", "Cardstock Heavyweight", "Sticky Notes Neon", "Notebook Spiral"],
        "Binders": ["3-Ring Binder 2-inch", "Heavy Duty Binder", "Presentation Folder Pack"],
        "Art": ["Crayola Colored Pencils", "Sketchbook Medium", "Acrylic Paint Set", "Watercolor Brushes"],
        "Appliances": ["Compact Refrigerator", "Microwave Oven 900W", "Air Purifier HEPA", "Coffee Maker Espresso"],
        "Envelopes": ["Manila Envelopes Pack", "Self-Seal Mailing Envelopes", "Bubble Mailers padded"],
        "Fasteners": ["Paper Clips Jumbo", "Binder Clips Assorted", "Rubber Bands Premium", "Push Pins Colorful"]
    }
    
    # Regions and States
    regions_states = {
        "Central": ["Illinois", "Texas", "Michigan", "Indiana", "Wisconsin"],
        "East": ["New York", "Pennsylvania", "Ohio", "Massachusetts", "Maryland"],
        "South": ["Florida", "Georgia", "North Carolina", "Virginia", "Tennessee"],
        "West": ["California", "Washington", "Colorado", "Arizona", "Oregon"]
    }
    
    # Generate dates over 3 years
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2026, 6, 25)
    delta_days = (end_date - start_date).days
    
    data = []
    
    for i in range(num_rows):
        # Date
        days_to_add = np.random.randint(0, delta_days)
        order_date = start_date + timedelta(days=days_to_add)
        
        # Customer ID
        cust_id = f"CUST-{np.random.randint(10000, 99999)}"
        
        # Order ID
        order_id = f"CA-{order_date.year}-{np.random.randint(100000, 999999)}"
        
        # Category, Sub-category, and Product
        category = np.random.choice(list(cat_subcat.keys()))
        sub_cat = np.random.choice(cat_subcat[category])
        product = np.random.choice(products[sub_cat])
        
        # Region and State
        region = np.random.choice(list(regions_states.keys()))
        state = np.random.choice(regions_states[region])
        
        # Sales and Profit
        # Let's make sales dependent on category and product type
        base_sales = {
            "Technology": 400.0,
            "Furniture": 250.0,
            "Office Supplies": 45.0
        }[category]
        
        sales = np.round(np.random.exponential(base_sales) + 5.0, 2)
        
        # Profit can be positive or negative (average margin ~15%)
        mean_margin = {
            "Technology": 0.22,
            "Furniture": 0.05,
            "Office Supplies": 0.15
        }[category]
        
        margin = np.random.normal(mean_margin, 0.18)
        # Cap margin between -0.8 and 0.5
        margin = np.clip(margin, -0.8, 0.5)
        profit = np.round(sales * margin, 2)
        
        data.append({
            "Order ID": order_id,
            "Customer ID": cust_id,
            "Order Date": order_date.strftime("%Y-%m-%d"),
            "Product": product,
            "Category": category,
            "Sub-Category": sub_cat,
            "Region": region,
            "State": state,
            "Sales": sales,
            "Profit": profit
        })
        
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Generated mock data with {len(df)} rows and saved to {filename}")

if __name__ == "__main__":
    create_mock_superstore()
