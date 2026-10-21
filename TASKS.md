# ShopLite — Task List

Read [README.md](README.md) first and get the project running locally.

The assignment has **10 frontend tasks (FE-1 … FE-10)**, listed first, followed by **10 backend
tasks (BE-1 … BE-10)**.
**Your recruiter will tell you which track to complete.** If no track was specified, do as much as
you can, in order, and prioritise *quality over quantity*. A few well-built, well-tested tasks beat
many half-finished ones.

| Track                 | Tasks to complete                                        | Suggested time |
|-----------------------|----------------------------------------------------------|----------------|
| Frontend — Junior     | FE-1, FE-2, FE-3, FE-6                                   | 4–6 hours      |
| Frontend — Mid/Senior | FE-1 … FE-10                                             | 1–1.5 days     |
| Backend — Junior      | BE-1, BE-2, BE-3, BE-5                                   | 4–6 hours      |
| Backend — Mid-level   | BE-1 … BE-7                                              | 1–1.5 days     |
| Backend — Senior      | BE-1, BE-4, BE-6, BE-8, BE-9, BE-10                      | 1.5–2 days     |
| Full-stack            | FE-2 … FE-5, FE-7 and BE-1 … BE-4, BE-6                  | 1.5–2 days     |

### How frontend and backend tasks fit together

- **Frontend tasks** own templates, CSS and JavaScript: layout, styling, interaction, accessibility.
- **Backend tasks** own Python code: models, views, forms, services, REST API, migrations and tests.
  They may use minimal, unstyled templates just to make their pages work.
- Some frontend tasks depend on a backend task. Each backend task defines a **contract** (template
  context variables, URL names, JSON shapes). If the backend task it depends on is *not* in your
  track, build against the contract and add the smallest possible backend stub to make it work —
  mention this in `NOTES.md`. Stubs are not graded as backend work.

---

## General requirements (apply to every task)

- [ ] Code is clean, readable and consistent with the existing style (PEP 8 for Python).
- [ ] No breaking changes to existing behaviour unless a task asks for it; all tests pass: `python manage.py test`.
- [ ] Small, focused commits with meaningful messages.
- [ ] A `NOTES.md` file describing your decisions, trade-offs, assumptions, and what you would do with more time.

**Frontend tasks additionally:**
- [ ] No build step: plain HTML templates, CSS and vanilla JavaScript (no frameworks or CDNs required).
- [ ] Works in current Chrome, Firefox and Edge, at widths from 360 px to 1440 px.
- [ ] Semantic HTML, keyboard accessible, visible focus states, images have `alt` text.
- [ ] Core flows (browse, add to cart, checkout) still work with JavaScript disabled (progressive enhancement).

**Backend tasks additionally:**
- [ ] Every task has automated tests. Bug fixes include a **regression test** that fails before the fix.
- [ ] Database changes are delivered as migrations.
- [ ] Money is handled with `Decimal`, never `float`.

---

# Frontend tasks

### FE-1 Responsive header and mobile navigation
- [ ] Below 760 px the navigation collapses into a menu button ("hamburger") that opens/closes the menu.
- [ ] The menu button has correct `aria-expanded` / `aria-controls`, works with the keyboard, and closes on <kbd>Esc</kbd>.
- [ ] The header stays visible while scrolling (sticky) without covering page content.
- [ ] The cart badge stays visible at all widths.

### FE-2 Catalogue controls: search, sort and pagination UI
*Depends on: BE-2 (contract).*
- [ ] Search box above the product grid; keeps the current query after submitting.
- [ ] Sort dropdown that applies immediately on change (and still works without JavaScript via a submit button).
- [ ] Pagination controls: previous / next, page numbers, current page highlighted, disabled states at the ends.
- [ ] All controls preserve each other's state and the current category.
- [ ] A friendly empty state when nothing matches, with a "clear search" link.

### FE-3 Product cards and product page
- [ ] "Out of stock" badge when `stock == 0`, and "Only N left" when stock is 5 or fewer.
- [ ] Out-of-stock products show a disabled "Add to cart" button with an explanation.
- [ ] Replace the quantity `<select>` with a −/+ quantity stepper that cannot go below 1 or above the available stock (falls back to a normal number input without JavaScript).
- [ ] Consistent card heights, hover/focus states, and lazy-loaded images (`loading="lazy"`).

### FE-4 Add to cart without page reload
*Depends on: BE-6 (contract).*
- [ ] "Add to cart" on the product page and product cards uses `fetch()` against `POST /api/cart/items/`.
- [ ] The header cart badge updates immediately; a toast notification confirms success or shows the error `detail`.
- [ ] CSRF is handled correctly; the button shows a loading state and prevents double clicks.
- [ ] Without JavaScript, the normal form POST still works.

### FE-5 Interactive cart page
*Depends on: BE-6 (contract); coupon part depends on BE-10.*
- [ ] Changing a quantity or removing an item updates line totals, cart total and the header badge **without a page reload**.
- [ ] Removing an item offers an "Undo" for a few seconds.
- [ ] A well-designed empty-cart state.
- [ ] Coupon input with apply/remove, showing discount and new total (if BE-10 is available; otherwise build against its contract).
- [ ] Changes are announced to screen readers (`aria-live`).

### FE-6 Checkout form experience
- [ ] Client-side validation (required fields, email format, postal code) with inline error messages next to each field — server-side errors are displayed in the same style.
- [ ] Correct `autocomplete` attributes (`name`, `email`, `street-address`, `address-level2`, `postal-code`).
- [ ] The "Place order" button is disabled after the first click to prevent duplicate orders.
- [ ] The order summary is sticky on desktop and collapsible on mobile.

### FE-7 Order confirmation and order history pages
*Depends on: BE-4 and BE-5 (contracts).*
- [ ] Order confirmation page: thank-you message, order number, items, total, shipping address.
- [ ] Order history: list/table of orders with colour-coded status badges (pending / paid / shipped / cancelled).
- [ ] Order detail page with line items; layout works on mobile (no horizontal scrolling).
- [ ] "My orders" link in the header for logged-in users.

### FE-8 Account and authentication pages
*Profile part depends on: BE-5 (contract).*
- [ ] Restyle login and register pages: clear labels, inline errors, helpful password requirements.
- [ ] "Show password" toggle on password fields (accessible, keyboard operable).
- [ ] Password strength indicator on the register page (purely client-side guidance).
- [ ] Style the "My account" profile page and link it from the header.

### FE-9 Live search suggestions
*Depends on: BE-2 (API part).*
- [ ] While typing in the search box, show up to 5 suggestions from `/api/products/?search=…`.
- [ ] Requests are debounced (~300 ms) and out-of-order responses never overwrite newer results.
- [ ] Full keyboard support: <kbd>↑</kbd>/<kbd>↓</kbd> to move, <kbd>Enter</kbd> to open, <kbd>Esc</kbd> to close; follows the ARIA combobox pattern.
- [ ] Pressing <kbd>Enter</kbd> without a highlighted suggestion submits the normal search.

### FE-10 Accessibility audit and dark mode
- [ ] Run an accessibility audit (e.g. Lighthouse / axe) on the product list, product, cart and checkout pages and fix the issues found. Target: Lighthouse accessibility score ≥ 95.
- [ ] Colour contrast meets WCAG AA; add a "Skip to content" link.
- [ ] Dark theme that follows `prefers-color-scheme`, plus a toggle in the header; the choice is remembered (`localStorage`).
- [ ] Document the audit results (before/after) in `NOTES.md`.

---

# Backend tasks

### BE-1 Bug report: cart quantities
> *"When I click 'Add to cart' twice for the same product (quantity 1 each time), my cart only
> contains 1 item instead of 2."* — customer support ticket #482

- [ ] Find the root cause and fix it.
- [ ] Updating the quantity on the cart page must still **replace** the quantity (not add to it).
- [ ] Add a regression test.

### BE-2 Catalogue search, sorting and pagination
- [ ] `GET /?q=<text>` filters products whose **name or description** contains the text (case-insensitive).
- [ ] `?sort=` accepts `newest` (default), `price_asc`, `price_desc`, `name`. Unknown values fall back to the default — never an error.
- [ ] 8 products per page via `?page=`; invalid or out-of-range pages are handled gracefully.
- [ ] Search, sorting, pagination and the category filter all combine.
- [ ] The products API supports the same: `/api/products/?search=…&ordering=…&category=<slug>`.
- **Contract** (`catalog:product_list` template context):
  `products` (current page), `page_obj`, `query` (str), `sort` (str),
  `sort_options` (list of `(value, label)` tuples), `category`, `categories`.

### BE-3 Stock validation
- [ ] It must be impossible to put more units of a product in the cart than are in stock — including via
      repeated adds, the quantity update form, or a crafted POST.
- [ ] Out-of-stock and inactive products cannot be added.
- [ ] On rejection, the user is redirected back with an error message (Django messages framework).

### BE-4 Checkout
The checkout form at `/orders/checkout/` renders but does not create orders.
- [ ] Implement a service function `create_order(user, cart, shipping_data) -> Order` in `apps/orders/services.py`.
- [ ] Creates an `Order` for the user plus one `OrderItem` per cart line.
- [ ] Item prices come from the **current product price in the database**, not from the session.
- [ ] Decrements stock. If any product has insufficient stock, **no** order is created and the user is told which product(s).
- [ ] The operation is atomic, and stock can never be oversold — even when two customers buy the last unit at the same moment. Explain your approach in `NOTES.md`.
- [ ] Clears the cart and redirects to the order confirmation page.
- **Contract:** on success, redirect to `orders:order_detail` (`/orders/<id>/`) — see BE-5.

### BE-5 Order history and profile
- [ ] `/orders/` lists the logged-in user's orders, newest first.
- [ ] `/orders/<id>/` shows a single order. A user must **never** be able to see another user's order (respond with 404).
- [ ] `/accounts/profile/` lets the logged-in user view and update first name, last name and email.
- [ ] All three pages require login.
- **Contract:**
  - `orders:order_list` → context `orders` (each with `item_count` and `total` available)
  - `orders:order_detail` → context `order` (with `order.items` and `order.get_total_cost`)
  - `accounts:profile` → context `form`; success redirects back with a success message

### BE-6 Cart REST API
Expose the cart so JavaScript clients can use it (session authentication).
- [ ] `GET    /api/cart/`
- [ ] `POST   /api/cart/items/` — body `{"product": <id>, "quantity": <n>}` adds to the cart
- [ ] `PATCH  /api/cart/items/<product_id>/` — body `{"quantity": <n>}` sets the quantity
- [ ] `DELETE /api/cart/items/<product_id>/` — removes the item
- [ ] Validation and correct status codes (201/200/204, 400 for invalid quantity or insufficient stock, 404 for unknown product).
- [ ] Reuse the existing `Cart` class — don't duplicate cart logic.
- **Contract** — every successful response (except 204) returns the full cart:
  ```json
  {
    "items": [
      {"product": {"id": 1, "name": "Yoga Mat", "slug": "yoga-mat", "url": "/product/yoga-mat/"},
       "quantity": 2, "unit_price": "24.99", "line_total": "49.98"}
    ],
    "total_items": 2,
    "total_price": "49.98"
  }
  ```
  Errors return `{"detail": "<human readable message>"}`.

### BE-7 Orders REST API
- [ ] `GET /api/orders/` and `GET /api/orders/<id>/` — authenticated users see **only their own** orders.
- [ ] `POST /api/orders/` — places an order from the current cart (shipping details in the body), reusing the BE-4 service.
- [ ] Clients cannot set prices, status or the order owner.
- [ ] Anonymous requests receive 401/403.
- [ ] Document the endpoints (section in `NOTES.md`, or OpenAPI via `drf-spectacular`).

### BE-8 Performance
Operations reports that the product list page and the products API get slower as the catalogue grows.
- [ ] Investigate, identify the cause(s) and fix them. Check the order pages too.
- [ ] Prove the fix with tests (e.g. `assertNumQueries`) that would catch a regression.
- [ ] Add database indexes where they are justified.
- [ ] Explain your findings in `NOTES.md`.

### BE-9 API security review
- [ ] Review the public REST API and fix anything that should not be exposed or allowed.
- [ ] Add tests that lock the fix in place.
- [ ] Write a short security review in `NOTES.md` covering other risks you found in the project
      (fixed or not), each with a severity and a recommended fix.

### BE-10 Discount coupons
- [ ] `Coupon` model: code (case-insensitive), percentage **or** fixed-amount discount, validity window, active flag, optional maximum number of uses. Manageable in the Django admin.
- [ ] Apply / remove a coupon for the current cart; invalid, expired or used-up coupons are rejected with a clear message.
- [ ] The order stores the coupon and discount amount. Totals are never negative and are rounded to 2 decimal places with a clearly defined rounding mode.
- [ ] Coupon usage is counted at checkout, not when the coupon is applied.
- **Contract:**
  - `POST /cart/coupon/apply/` (form field `code`) and `POST /cart/coupon/remove/`; both redirect to the cart page
  - Cart object exposes `cart.coupon`, `cart.get_discount()`, `cart.get_total_price_after_discount()`
  - `GET /api/cart/` additionally returns `"coupon"`, `"discount"` and `"total_after_discount"`

---

## Submission

1. Push your work to a **private** Git repository (or send a `.zip` without `db.sqlite3` / virtualenvs).
2. Include `NOTES.md` with:
   - which tasks you completed (and which you skipped or only partially completed),
   - any backend stubs you added for frontend tasks,
   - design decisions and trade-offs,
   - anything you noticed in the codebase that you would improve,
   - roughly how much time you spent.
3. Make sure a reviewer can run `pip install -r requirements.txt && python manage.py migrate && python manage.py seed_data && python manage.py test` from a fresh clone.

Good luck — and have fun!
