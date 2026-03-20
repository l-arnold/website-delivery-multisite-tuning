# website_delivery_website_filter

Odoo 14 module that corrects website context on sale orders at checkout and
filters shipping carriers by website. Solves multi-website delivery method
display issues where carriers from the wrong website appear at checkout.

Also known as: `website-delivery-multisite-tuning` (GitHub repository name)

## Naming Note

The GitHub repository is named `website-delivery-multisite-tuning`.
The Odoo module technical name and server directory are both
`website_delivery_website_filter`. A symlink exists on the production server:

```
/opt/odoo/addons_extra/website_delivery_multisite_tuning
    → /opt/odoo/addons_extra/website_delivery_website_filter
```

Long-term goal is to align the naming. Until then, use the symlink for
navigation clarity. The Odoo module name (`website_delivery_website_filter`)
is what matters for upgrades and dependency declarations.

## What It Does

### Website context correction
When a customer's session carries a sale order from one website into a
checkout on a different website (e.g. navigating from `nomadic.net` to
`erp.nomadic.net`), Odoo does not automatically update the order's
`website_id`. This module detects the mismatch and corrects it.

Cross-company mismatches are detected but **not** corrected — a Nomadic Inc.
order will not be updated to a Full Circle Paddles website context. Those
sessions need a fresh order.

### Website-based carrier filtering
Filters the published carrier list to only show carriers assigned to the
current website, plus carriers with no website assigned (which show on all
websites for their company).

### Order context injection for packaging filter
Injects the current sale order into the carrier evaluation context so that
`delivery_smart_packaging` can access the correct order for dimension-based
filtering. This coordination is the reason both modules must be installed
together — the MRO between them is intentional.

## How It Coordinates With delivery_smart_packaging

The call chain at checkout:

```
website_delivery_website_filter._get_delivery_methods(order)
  ↓ corrects website_id if mismatched
  ↓ filters carriers by website
  ↓ injects order_id into context
  → carriers.available_carriers(address)
      ↓ (in delivery_smart_packaging)
      ↓ reads order_id from context
      ↓ finds minimum viable box for order's products
      → returns filtered carrier list
```

The `order_id` context injection happens in this module's
`_get_delivery_methods()` rather than in `delivery_smart_packaging` to
avoid MRO conflicts. Both modules override the same base method — having
only one override (here) and calling `carriers.available_carriers()` directly
ensures the context survives the full call chain.

## Known Limitations

### Company traversal via blank website
Carriers with no `website_id` set are shown on all websites for their
company. However, if a carrier has `company_id` set to Company A and no
`website_id`, it will currently appear on Company B websites as well.
A future enhancement would add company-aware filtering to the carrier search.

### Many-to-one website assignment
Currently `delivery.carrier` supports only one website per carrier record
(`Many2one`). Ideally carriers would support multiple website assignments
(`Many2many`) similar to how products handle `website_ids`. This would
significantly reduce the number of carrier records needed in multi-website
setups.

## Session History

This module was developed and refined in a March 2026 session addressing:
- Multi-website carrier filtering (original)
- Website context correction for cross-site navigation
- MRO coordination with `delivery_smart_packaging`
- Cross-company mismatch detection

## Repositories

- This module: https://github.com/l-arnold/website-delivery-multisite-tuning
- Companion module: https://github.com/l-arnold/delivery-smart-packaging

## License

LGPL-3