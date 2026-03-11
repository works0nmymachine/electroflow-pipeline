# Data Generation Specs

Rules and logic behind the mock data generators.

## Customers

- Country selection is weighted by GDP (70% Nominal, 30% Per Capita)
- Names, cities, and postcodes are generated using localized Faker providers so they match the country
- Phone numbers use the correct international dial code
- Built-in data quality issues for practice: 10% missing phone numbers, mixed date formats, 5% duplicate records

## Products

- Modeled after the Belsimpel product catalog: smartphones, audio/wearables, and accessories
- Real-ish brand names and model names (Apple, Samsung, Google, etc.)
- 6-digit numerical product IDs

## Orders

- Nested JSON format — each order contains a list of 1–4 items
- Every `customer_id` and `product_id` references a real record (enforced by `integrity_utils.py`)
- Includes funnel timestamps: purchase → approved → shipped → delivered
- Financial fields like `unit_price` and `subtotal` are intentionally excluded — those calculations happen in the Gold layer

## Payments

- 1 payment method per order
- Only Klarna supports installments (3, 6, or 12 months)
- Payment value is calculated from the product prices × quantities + shipping + tax

## Coupons

- Campaign-based (Black Friday, Cyber Monday, etc.)
- Each campaign generates 3–8 coupon variants with different discount percentages

## Output

All generated files go to `data/raw/`. This folder is in `.databricksignore` so it doesn't sync to the Databricks workspace.
