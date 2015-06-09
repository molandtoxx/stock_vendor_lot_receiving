from openerp.osv import osv, fields
from openerp.tools.translate import _

class StockVendorLotAssignVendorWizard(osv.osv):
    _name = 'stock.vendor.lot.create.mass.wizard'
    _columns = {
	'name': fields.char('Name'),
	'vendor':fields.many2one('res.partner', 'Vendor'),
	'number_lots': fields.integer('Number of Lots'),
	'purchase': fields.many2one('purchase.order', 'Purchase Order'),
    }

    def default_get(self, cr, uid, fields, context=None):
        if context is None: context = {}
	lots = context.get('active_ids')
	items = []
	for item in lots:
	    items.append({'lot': item})

	res = {}
	res.update(lots=items)
        return res


    def create_new_licenseplate(self, cr, uid, wizard, receipt):
        lot_obj = self.pool.get('stock.vendor.lot')
        if wizard:
            vals = {
                    'vendor': wizard.vendor.id if wizard.vendor else False,
		    'purchase': wizard.purchase.id if wizard.purchase else False,
		    'receipt': receipt.id,
            }

        else:
            vals = {}

        lot_id = lot_obj.create(cr, uid, vals)
        return lot_obj.browse(cr, uid, lot_id)


    def mass_create_vendor_lots(self, cr, uid, ids, context=None):
	wizard = self.browse(cr, uid, ids[0])
	receipt_obj = self.pool.get('stock.vendor.receipt')
	receipt = receipt_obj.browse(cr, uid, context.get('active_id'))
	for x in range(wizard.number_lots):
	    self.create_new_licenseplate(cr, uid, wizard, receipt)

	return True
	    
