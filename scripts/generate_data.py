"""
Zawadi Retail - synthetic data generator (medallion architecture practice project).

Creates the CSV files that will live in the GitHub repo and be ingested into Fabric.
Run:  python generate_data.py <output_folder>
The random seed is fixed, so everyone gets identical files.
"""
import csv
import os
import random
import sys
from datetime import date, datetime, timedelta

random.seed(42)
OUT = sys.argv[1] if len(sys.argv) > 1 else "repo"


def write_csv(path, header, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


# ---------------------------------------------------------------- regions
regions = [
    ("R01", "Nairobi", "Achieng Otieno"),
    ("R02", "Coast", "Hamisi Mwangi"),
    ("R03", "Western", "Wanjiru Kamau"),
    ("R04", "Rift Valley", "Kiprono Koech"),
    ("R05", "Central", "Njeri Mutua"),
]
write_csv(f"{OUT}/data/reference/regions.csv",
          ["region_id", "region_name", "regional_manager"], regions)

# ----------------------------------------------------------------- stores
store_defs = [
    ("S01", "Zawadi Westlands", "R01", "Nairobi", "Flagship", "2018-03-12"),
    ("S02", "Zawadi Kilimani", "R01", "Nairobi", "Standard", "2019-06-01"),
    ("S03", "Zawadi Eastleigh", "R01", "Nairobi", "Standard", "2020-02-17"),
    ("S04", "Zawadi Nyali", "R02", "Mombasa", "Flagship", "2018-09-30"),
    ("S05", "Zawadi Diani", "R02", "Kwale", "Express", "2021-12-05"),
    ("S06", "Zawadi Kisumu CBD", "R03", "Kisumu", "Standard", "2019-11-11"),
    ("S07", "Zawadi Kakamega", "R03", "Kakamega", "Express", "2022-04-20"),
    ("S08", "Zawadi Nakuru", "R04", "Nakuru", "Flagship", "2019-01-15"),
    ("S09", "Zawadi Eldoret", "R04", "Eldoret", "Standard", "2020-08-08"),
    ("S10", "Zawadi Naivasha", "R04", "Naivasha", "Express", "2023-03-03"),
    ("S11", "Zawadi Thika", "R05", "Thika", "Standard", "2021-05-25"),
    ("S12", "Zawadi Nyeri", "R05", "Nyeri", "Standard", "2022-10-10"),
]
write_csv(f"{OUT}/data/reference/stores.csv",
          ["store_id", "store_name", "region_id", "city", "store_type", "opened_date"],
          store_defs)
store_ids = [s[0] for s in store_defs]

# --------------------------------------------------------------- products
catalog = {
    "Beverages": {"Tea": ["Kericho Gold", "Ketepa"], "Coffee": ["Dormans", "Java House"],
                  "Juice": ["Del Monte", "Minute Maid"], "Water": ["Dasani", "Keringet"]},
    "Bakery": {"Bread": ["Broadways", "Festive"], "Biscuits": ["Pioneer", "Britania"]},
    "Dairy": {"Milk": ["Brookside", "Tuzo"], "Yoghurt": ["Daima", "Fresha"]},
    "Household": {"Cleaning": ["Omo", "Jik"], "Paper": ["Kleenex", "Rosy"]},
    "Personal Care": {"Soap": ["Geisha", "Dettol"], "Oral Care": ["Colgate", "Oral-B"]},
}
products = []
n = 1
for cat, subs in catalog.items():
    for sub, brands in subs.items():
        for brand in brands:
            for size in ("Small", "Large"):
                price = random.choice([45, 60, 85, 120, 150, 210, 280, 350, 480])
                if size == "Large":
                    price = int(price * 1.6)
                cost = round(price * random.uniform(0.55, 0.75), 2)
                products.append([f"P{n:03d}", f"{brand} {sub} {size}", cat, sub, brand,
                                 f"{price:.2f}", f"{cost:.2f}"])
                n += 1
# products_day1: add dirty rows (messy casing/spacing + one exact duplicate)
day1_products = [r[:] for r in products]
day1_products[3][2] = "  beverages "      # inconsistent casing / spaces
day1_products[10][2] = "DAIRY"
day1_products.append(day1_products[5][:])  # exact duplicate row
write_csv(f"{OUT}/data/products/products_day1.csv",
          ["product_id", "product_name", "category", "subcategory", "brand",
           "unit_price", "unit_cost"], day1_products)

# products_day2: a few price changes (to show MERGE updates) + 4 new products
day2_products = [r[:] for r in products]
for idx in (0, 7, 15, 22, 30):
    old = float(day2_products[idx][5])
    day2_products[idx][5] = f"{round(old * 1.08):.2f}"   # +8% price increase
for k in range(4):
    n += 1
    day2_products.append([f"P{len(products) + k + 1:03d}", f"Zawadi Own Brand {k + 1}",
                          "Household", "Cleaning", "Zawadi", "99.00", "60.00"])
write_csv(f"{OUT}/data/products/products_day2.csv",
          ["product_id", "product_name", "category", "subcategory", "brand",
           "unit_price", "unit_cost"], day2_products)
prod_ids_day1 = [p[0] for p in products]
prod_ids_day2 = [p[0] for p in day2_products]
price_day1 = {p[0]: float(p[5]) for p in products}
price_day2 = {p[0]: float(p[5]) for p in day2_products}

# -------------------------------------------------------------- customers
first = ["Wanjiku", "Otieno", "Amina", "Kevin", "Mercy", "Brian", "Faith", "Peter", "Grace",
         "John", "Esther", "Dennis", "Lucy", "Samuel", "Naomi", "James", "Ruth", "Victor",
         "Joyce", "Collins"]
last = ["Mwangi", "Odhiambo", "Hassan", "Kiplagat", "Njoroge", "Wekesa", "Achieng", "Mutiso",
        "Chebet", "Kariuki", "Omondi", "Barasa", "Wairimu", "Maina", "Nyambura"]
cities = ["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret", "Thika", "Nyeri", "Kakamega"]
segments = ["Regular", "Silver", "Gold"]

customers = []
for i in range(1, 301):
    fn, ln = random.choice(first), random.choice(last)
    signup = date(2022, 1, 1) + timedelta(days=random.randint(0, 1000))
    phone = f"07{random.randint(10000000, 99999999)}"
    customers.append([f"C{i:04d}", fn, ln, f"{fn}.{ln}{i}@example.com".lower(),
                      phone, random.choice(cities), random.choice(segments), signup.isoformat()])
day1_customers = [r[:] for r in customers]
day1_customers[4][3] = day1_customers[4][3].upper()   # dirty email casing
day1_customers[9][4] = ""                              # missing phone
day1_customers[20][5] = "nairobi "                     # dirty city
write_csv(f"{OUT}/data/customers/customers_day1.csv",
          ["customer_id", "first_name", "last_name", "email", "phone", "city", "segment",
           "signup_date"], day1_customers)

# customers_day2 = full snapshot: 25 customers changed city/segment (-> SCD2 history),
# 15 brand-new customers
day2_customers = [r[:] for r in customers]
changed = random.sample(range(len(day2_customers)), 25)
for idx in changed:
    row = day2_customers[idx]
    if idx % 2 == 0:
        row[5] = random.choice([c for c in cities if c != row[5]])        # moved city
    else:
        row[6] = {"Regular": "Silver", "Silver": "Gold", "Gold": "Gold"}[row[6]]  # upgraded
for i in range(301, 316):
    fn, ln = random.choice(first), random.choice(last)
    day2_customers.append([f"C{i:04d}", fn, ln, f"{fn}.{ln}{i}@example.com".lower(),
                           f"07{random.randint(10000000, 99999999)}", random.choice(cities),
                           "Regular", "2026-11-08"])
write_csv(f"{OUT}/data/customers/customers_day2.csv",
          ["customer_id", "first_name", "last_name", "email", "phone", "city", "segment",
           "signup_date"], day2_customers)

# ------------------------------------------------------------------ sales
payment = ["M-Pesa", "Cash", "Card"]
dirty_payment = {"M-Pesa": ["mpesa", "M-PESA"], "Cash": ["cash"], "Card": ["CARD"]}
order_counter = 100000


def make_day(d, cust_pool, prod_pool, price_by_id, lines_target=600):
    """Generate one day of order lines. Returns list of rows."""
    global order_counter
    rows = []
    while len(rows) < lines_target:
        order_counter += 1
        order_id = f"O{order_counter}"
        store = random.choice(store_ids)
        cust = random.choice(cust_pool) if random.random() > 0.03 else ""   # ~3% walk-ins
        ts = datetime(d.year, d.month, d.day, random.randint(8, 20), random.randint(0, 59),
                      random.randint(0, 59))
        pay = random.choice(payment)
        if random.random() < 0.05:                                          # ~5% dirty casing
            pay = random.choice(dirty_payment[pay])
        for line_no in range(1, random.randint(1, 5) + 1):
            pid = random.choice(prod_pool)
            qty = random.randint(1, 6)
            disc = random.choice([0, 0, 0, 5, 10, 15])
            rows.append([order_id, line_no, d.isoformat(), ts.strftime("%Y-%m-%d %H:%M:%S"),
                         cust, pid, store, qty, f"{price_by_id[pid]:.2f}", disc, pay])
    # ~1% exact duplicate lines (simulate a source system re-sending records)
    for r in random.sample(rows, max(1, len(rows) // 100)):
        rows.append(r[:])
    random.shuffle(rows)
    return rows


sales_header = ["order_id", "order_line_no", "order_date", "order_timestamp", "customer_id",
                "product_id", "store_id", "quantity", "unit_price", "discount_pct",
                "payment_method"]
cust_ids_day1 = [c[0] for c in customers]
cust_ids_day2 = [c[0] for c in day2_customers]

start = date(2026, 11, 1)
for k in range(7):                       # files for days 1-7 = initial load
    d = start + timedelta(days=k)
    write_csv(f"{OUT}/data/sales/sales_{d.isoformat()}.csv", sales_header,
              make_day(d, cust_ids_day1, prod_ids_day1, price_day1))
d8 = start + timedelta(days=7)           # day 8 = "day-2 simulation" file; can use new IDs
write_csv(f"{OUT}/data/sales/sales_{d8.isoformat()}.csv", sales_header,
          make_day(d8, cust_ids_day2, prod_ids_day2, price_day2))

print("done ->", OUT)
