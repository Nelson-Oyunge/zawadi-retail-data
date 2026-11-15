# zawadi-retail-data

Synthetic retail data for a Microsoft Fabric medallion architecture practice project.

- `data/sales/`      daily order-line files (2026-11-01 to 2026-11-07 = initial load, 2026-11-08 = day-2 simulation)
- `data/products/`   products_day1.csv (initial) and products_day2.csv (price changes + new products)
- `data/customers/`  customers_day1.csv (initial) and customers_day2.csv (full snapshot with changes + new customers)
- `data/reference/`  stores.csv and regions.csv
- `scripts/`         generate_data.py (recreates all files, seed = 42)

All data is fictional. Some records are deliberately dirty (duplicates, blanks, inconsistent casing).
