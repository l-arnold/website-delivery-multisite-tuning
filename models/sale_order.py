from odoo import models
import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _get_delivery_methods(self):
        _logger.info("=" * 80)
        _logger.info("CUSTOM WEBSITE FILTER: _get_delivery_methods called")
        _logger.info(f"Order ID: {self.id}, Website ID: {self.website_id.id if self.website_id else None}")
        
        address = self.partner_shipping_id
        
        # Get all published carriers
        all_carriers = self.env['delivery.carrier'].sudo().search([
            ('website_published', '=', True)
        ])
        _logger.info(f"Found {len(all_carriers)} published carriers BEFORE filtering")
        
        # Filter by website
        if self.website_id:
            carriers = all_carriers.filtered(
                lambda c: not c.website_id or c.website_id == self.website_id
            )
            _logger.info(f"After website filter: {len(carriers)} carriers for website {self.website_id.id}")
        else:
            carriers = all_carriers
            _logger.info("No website_id on order, showing all carriers")
        
        _logger.info(f"Carrier IDs: {carriers.ids}")
        _logger.info("=" * 80)
        
        return carriers.available_carriers(address)