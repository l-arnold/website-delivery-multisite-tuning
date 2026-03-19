from odoo import models
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _get_delivery_methods(self):
        _logger.info("=" * 80)
        _logger.info("CUSTOM WEBSITE FILTER: _get_delivery_methods called")
        _logger.info(f"Order ID: {self.id}, Website ID: {self.website_id.id if self.website_id else None}")

        # If the order's website doesn't match the current website context,
        # update it. This happens when a user navigates between sites while
        # carrying an existing session/order (e.g. nomadic.net → erp.nomadic.net).
        try:
            current_website = self.env['website'].get_current_website()
            if current_website and self.website_id != current_website:
                _logger.info(
                    f"Order {self.id}: website mismatch — "
                    f"order has website {self.website_id.id}, "
                    f"current context is website {current_website.id}. Updating."
                )
                self.sudo().write({'website_id': current_website.id})
        except Exception as e:
            # Never block delivery method lookup due to website sync errors
            _logger.warning(f"Order {self.id}: could not sync website context: {e}")

        address = self.partner_shipping_id
        order_company = self.company_id

        # Get all published carriers, pre-filtered by company.
        # Carriers with no company set are treated as available to all companies.
        all_carriers = self.env['delivery.carrier'].sudo().search([
            ('website_published', '=', True),
            '|',
            ('company_id', '=', False),
            ('company_id', '=', order_company.id),
        ])
        _logger.info(
            f"Found {len(all_carriers)} published carriers BEFORE filtering "
            f"(company: {order_company.name}, id: {order_company.id})"
        )

        # Filter by website within the company-filtered set.
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

        return carriers.available_carriers(address)