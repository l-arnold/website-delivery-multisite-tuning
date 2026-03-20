from odoo import models
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _get_delivery_methods(self):
        _logger.info("=" * 80)
        _logger.info("CUSTOM WEBSITE FILTER: _get_delivery_methods called")
        _logger.info(
            f"Order ID: {self.id}, "
            f"Website ID: {self.website_id.id if self.website_id else None}"
        )

        # If the order's website doesn't match the current website context,
        # update it. Only update if same company — cross-company sessions
        # should not update (they need a fresh order).
        try:
            current_website = self.env['website'].get_current_website()
            if current_website and self.website_id != current_website:
                if current_website.company_id == self.company_id:
                    _logger.info(
                        f"Order {self.id}: website mismatch — "
                        f"order has website {self.website_id.id}, "
                        f"current context is website {current_website.id}. Updating."
                    )
                    self.sudo().write({'website_id': current_website.id})
                else:
                    _logger.warning(
                        f"Order {self.id}: cross-company website mismatch — "
                        f"order company {self.company_id.name} vs "
                        f"website company {current_website.company_id.name}. "
                        f"Not updating."
                    )
        except Exception as e:
            _logger.warning(f"Order {self.id}: could not sync website context: {e}")

        address = self.partner_shipping_id

        # Get all published carriers
        all_carriers = self.env['delivery.carrier'].sudo().search([
            ('website_published', '=', True)
        ])
        _logger.info(
            f"Found {len(all_carriers)} published carriers BEFORE filtering"
        )

        # Filter by website.
        # Carriers with no website assigned show on all websites for their company.
        if self.website_id:
            carriers = all_carriers.filtered(
                lambda c: not c.website_id or c.website_id == self.website_id
            )
            _logger.info(
                f"After website filter: {len(carriers)} carriers "
                f"for website {self.website_id.id}"
            )
        else:
            carriers = all_carriers
            _logger.info("No website_id on order, showing all carriers")

        _logger.info(f"Carrier IDs: {carriers.ids}")
        _logger.info("=" * 80)

        # Inject order_id into context so delivery_smart_packaging's
        # available_carriers override can access the correct order for
        # packaging dimension filtering.
        # This must happen here rather than in delivery_smart_packaging's
        # own _get_delivery_methods override to avoid MRO conflicts between
        # the two modules both overriding the same method.
        carriers = carriers.with_context(order_id=self)
        return carriers.available_carriers(address)