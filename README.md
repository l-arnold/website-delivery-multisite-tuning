# Website Delivery Multi-Website Tuning

Fixes Odoo 14.0.0 core bug where delivery methods ignore `website_id` filtering during checkout.

## Problem

In Odoo 14.0.0, the `_get_delivery_methods()` function in `website_sale_delivery` only checks `website_published=True`, not `website_id`. This causes delivery methods from other websites to appear incorrectly in multi-website setups.

## Solution

Overrides `sale.order._get_delivery_methods()` to properly filter carriers by website:
```python
if self.website_id:
    carriers = all_carriers.filtered(
        lambda c: not c.website_id or c.website_id == self.website_id
    )
```

## Installation

1. Copy module to `addons_extra/website_delivery_website_filter/`
2. Update Apps List
3. Install "Website Delivery - Multi-Website Filter Fix"
4. Test checkout on each website - should only show methods for that website

## Requirements

- Odoo 14.0
- `website_sale_delivery` (core)
- Multi-website setup with `delivery.carrier.website_id` assignments

## Status

✅ **Production Ready** - Deployed and tested on multi-website Odoo 14 e-commerce

## Author

Landis Arnold - Nomadic Inc.  
https://nomadic.net

## License

LGPL-3
