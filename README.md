# ShopLite — Python Developer Assessment

ShopLite is a small but realistic e-commerce web application (backend + frontend) built with
**Django** and **Django REST Framework**. It is intentionally *unfinished*: your job is to extend it,
fix it and improve it by working through the tasks in **[TASKS.md](TASKS.md)**.

## Tech stack

| Layer     | Technology                                                        |
|-----------|-------------------------------------------------------------------|
| Backend   | Python 3.12+, Django 6, Django REST Framework                     |
| Frontend  | Django templates, plain CSS, vanilla JavaScript (no build step)   |
| Database  | SQLite (development)                                              |
| Tests     | Django test runner (`python manage.py test`)                      |

## Getting started

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create the database and load sample data
python manage.py migrate
python manage.py seed_data          # add --reset to wipe catalog data first

# 4. (Optional) create an admin account
python manage.py createsuperuser

# 5. Run the development server
python manage.py runserver
```

Open <http://127.0.0.1:8000/>.

| What               | URL                                   |
|--------------------|---------------------------------------|
| Storefront         | http://127.0.0.1:8000/                |
| Admin              | http://127.0.0.1:8000/admin/          |
| REST API (browsable) | http://127.0.0.1:8000/api/          |

A demo customer is created by `seed_data`: **username** `demo`, **password** `DemoPass!2026`.

## Running the tests

```bash
python manage.py test
```

All existing tests must keep passing (unless a task explicitly changes the behaviour they cover).

## Project structure

```
.
├── config/                 # Project settings, root URLs, API router
├── apps/
│   ├── accounts/           # Registration, login, logout
│   ├── catalog/            # Categories & products: models, views, REST API, seed command
│   ├── cart/               # Session-based shopping cart
│   └── orders/             # Order models and (unfinished) checkout
├── templates/              # HTML templates (frontend)
├── static/                 # CSS and JavaScript
├── requirements.txt
└── TASKS.md                # <-- your assignment
```

## What already works

- Product catalogue with category filtering and product detail pages
- Session-based cart (add / update / remove, running total, header badge)
- User registration, login and logout
- Read-only REST API for categories and products (`/api/categories/`, `/api/products/`)
- Django admin for products, categories and orders
- `Order` / `OrderItem` models and a checkout form (the form does **not** create orders yet)

## Submission

See the *Submission* section at the bottom of [TASKS.md](TASKS.md).
