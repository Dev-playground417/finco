# ShopLite — Notes

## Summary

The storefront UI was redesigned. It takes its visual direction from the Odoo eCommerce storefront: a white layout, a plum accent colour, a category sidebar, a grey search and sort bar, category chips, borderless product cards with corner ribbons, and a checkout progress indicator. The work follows the frontend rules in `TASKS.md`:

- No build step, frameworks or CDNs: plain Django templates, CSS and vanilla JavaScript.
- Progressive enhancement: browsing, add to cart and checkout all work with JavaScript disabled.
- Layouts work from 360 px to 1440 px.

All existing tests pass (`python manage.py test`, 16 tests).

## Task status

| Task | Status | Notes |
|------|--------|-------|
| FE-1 Responsive header and mobile navigation | Done | Below 760 px the nav collapses behind a `<button>` with `aria-expanded` and `aria-controls`. Esc closes the menu and returns focus to the button. The header is sticky, with `scroll-padding-top` so anchor targets aren't hidden. The cart badge is visible at all widths. |
| FE-2 Catalogue controls | Partial | Done: a search box that keeps the query; a sort dropdown that applies on change, with a `<noscript>` Apply button; category links that keep the search and sort; a "no results" state with a Clear search link. **Missing: pagination.** |
| FE-3 Product cards and product page | Done | "Sold out" and "N left" (stock ≤ 5) corner ribbons on cards, and a stock status line on the product page. Out-of-stock products have a disabled button explained via `aria-describedby`. The −/+ stepper is bounded by `min(stock, 10)` and falls back to `<input type="number">` without JS. Cards have equal heights (grid), hover and focus states, and `loading="lazy"` images. |
| FE-4 Add to cart without reload | Not started | Depends on BE-6. |
| FE-5 Interactive cart page | Partial | Done: a designed empty-cart state; flash messages are announced through an `aria-live` region; the quantity `<select>` now has a label. The cart no longer auto-submits on every keypress; it uses an explicit Update button. **Missing: updates without page reload, Undo, coupon UI.** |
| FE-6 Checkout form experience | Partial | Done: `autocomplete` tokens (set in `OrderCreateForm.widgets`); server errors shown inline next to each field; "Place order" disabled after the first submit and re-enabled when the page is restored from the back/forward cache; sticky order summary on desktop. **Missing: client-side validation, collapsible summary on mobile.** |
| FE-7 Order confirmation and history | Not started | Depends on BE-4 and BE-5. |
| FE-8 Account and auth pages | Partial | Login and register pages restyled, with labels, required markers, inline errors and Django's password requirements. **Missing: show-password toggle, strength meter, profile page.** |
| FE-9 Live search suggestions | Not started | |
| FE-10 Accessibility and dark mode | Partial | Done: a "Skip to content" link; `:focus-visible` styles everywhere; a dark theme built only from the `:root` custom properties. It follows `prefers-color-scheme`, has a header toggle (`aria-pressed`), remembers the choice in `localStorage`, and an inline `<head>` script prevents a flash of the wrong theme. **Missing: a Lighthouse/axe audit and before/after scores.** Contrast has not been measured with a tool yet. |
| BE-2 Search, sorting, pagination | Partial (stub) | Added only so the FE-2 controls actually work. `?q=` filters on name or description (case-insensitive). `?sort=` uses an allow-list (`newest`, `price_asc`, `price_desc`, `name`), and unknown values fall back to `newest`. **Missing: pagination, `page_obj`, API filtering, tests.** |
| BE-8 Performance | Partial | Added `select_related("category")` to the product list query, which removes one query per product card. **Missing: an `assertNumQueries` regression test, the order pages, indexes.** |
| BE-1, BE-3–BE-7, BE-9, BE-10 | Not started | See "Issues noticed" below. |

## Backend stubs added for frontend work

- **`apps/catalog/views.py`:** search, allow-listed sorting and a `filter_qs` helper that keeps the search and sort when switching category. This follows the BE-2 contract for `query`, `sort` and `sort_options`. `page_obj` is still missing.
- **`apps/orders/forms.py`:** `autocomplete` attributes through widget `attrs`, so the template can keep rendering fields generically.

## Design decisions and trade-offs

- **Design tokens.** All colours are custom properties on `:root`. Dark mode only redefines those properties, so no component rules are duplicated.
- **Product images.** The seed data has no `image_url`, so cards show a line icon per category (`templates/includes/category_icon.html`) instead of a big initial letter. Real images are used automatically when `image_url` is set.
- **Whole-card click target.** The product title link is stretched over the card with `::after`. That gives one link per card instead of two (image plus title), which reduces tab stops and duplicate screen-reader announcements.
- **Reusable form field partial** (`templates/includes/form_field.html`). It renders the label, a required marker, the input, inline errors and help text the same way on login, register and checkout.
- **Cart quantity markup.** The cart quantity `<select>` is rendered by hand so each row gets a unique `id` and a `<label>`. The `<option value="N" selected>` markup is kept identical, so the existing test still passes.
- **Mobile nav.** The nav only collapses once JavaScript has added the `js` class to `<html>`. Without JS the links simply wrap, so nothing is ever unreachable.

## Issues noticed in the codebase (not fixed)

| Severity | Issue | Where | Recommended fix |
|----------|-------|-------|-----------------|
| High | The products API exposes the confidential `cost_price`, plus `is_active` and timestamps, because the serializer uses `fields = "__all__"`. | `apps/catalog/serializers.py` | Use an explicit field allow-list and add a test asserting `cost_price` is not in the response (BE-9). |
| High | `Cart.add()` replaces the quantity instead of adding to it when the product is already in the cart. | `apps/cart/cart.py` | Use `+=` in the non-override branch and add a regression test (BE-1). |
| High | There is no stock validation; the quantity form allows up to 10 regardless of stock. | `apps/cart/views.py`, `forms.py` | Validate on the server, both in the cart and atomically at checkout (BE-3, BE-4). |
| Medium | The cart keeps the price from when the item was added, so totals go stale if a price changes. | `apps/cart/cart.py` | Read prices from the database at checkout (BE-4) and refresh them in the cart. |
| Medium | The cart page will crash if a product in the session is deleted, and deactivated products remain in the cart. | `Cart.__iter__` | Filter by `is_active` and drop missing products from the session. |
| Medium | Insecure defaults: a hard-coded fallback `SECRET_KEY`, and `DEBUG` on by default. | `config/settings.py` | Require environment variables outside development; make `manage.py check --deploy` clean. |
| Low | Commented-out code in `settings.py` runs `config/setconfig.py` via `subprocess` at import time (the file is currently empty). | `config/settings.py` | Delete those lines and the empty file; settings should never execute scripts. |
| Low | `Order.get_total_cost()` loops over the items, which costs one query per order on list pages. | `apps/orders/models.py` | Use `prefetch_related("items")` or annotate the total (BE-8). |

## What I would do with more time

1. Pagination (BE-2/FE-2), then tests for search, sort and the query count.
2. Add to cart without reload, and an interactive cart (FE-4/FE-5), built on a cart API (BE-6).
3. Client-side checkout validation using the Constraint Validation API, and a collapsible mobile summary (FE-6).
4. Show-password toggle and strength meter (FE-8).
5. A Lighthouse/axe audit with before/after scores (FE-10).

## Screenshots

Twenty screenshots (desktop, mobile and dark mode) are in `docs/screenshots/redesign/`. Note that `.gitignore` excludes `/docs/`, so they are **not** included in a Git push. Send them separately, or remove that line from `.gitignore`.

## Time spent

_To be filled in._
