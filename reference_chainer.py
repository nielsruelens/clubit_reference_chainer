from openerp.osv import osv, fields

##############################################################################
#
#    This module allows the system to perform automated reference chaining
#    to help the user to clearly see the link between several documents.
#
#    The chaining goes as follows:
#    sale.order:client_order_ref (standard field) to
#    stock.picking(.out):order_reference (custom field) to
#    account.invoice:reference (standard field)
#
##############################################################################




##############################################################################
#
#    stock.picking + stock.picking.out
#
#    This class extends stock.picking and stock.picking.out to make it
#    receptive for the reference it'll receive from the Sales Order.
#
#    The reason this field is added in both classes is because the
#    inheritance mechanism between both classes is broken. See OpenERP for
#    complaints.
#
#    This class also redefines the _prepare_invoice() method since it is
#    this method that will actually create the Customer Invoice for us to
#    add the order_reference value to.
#
##############################################################################

class stock_picking(osv.Model):
    _name = "stock.picking"
    _inherit = "stock.picking"
    _columns = {
        'order_reference': fields.char('Order reference', required=False, readonly=False),
    }


    ''' stock.picking:_prepare_invoice()
        --------------------------------
        This method is extended to make sure the Delivery Order reference is
        chained during the automated Customer Invoice creation. This automated
        creation happens using the stock.invoice.onshipping Wizard.
        ---------------------------------------------------------------------- '''
    def _prepare_invoice(self, cr, uid, picking, partner, inv_type, journal_id, context=None):

        result = super(stock_picking,self)._prepare_invoice(cr, uid, picking, partner, inv_type, journal_id, context)
        result['reference'] = picking.order_reference
        return result



class stock_picking_out(osv.Model):
    _name = "stock.picking.out"
    _inherit = "stock.picking.out"
    _columns = {
        'order_reference': fields.char('Order reference', required=False, readonly=False),
    }




##############################################################################
#
#    sale.order
#
#    This class extends sale.order to chain the reference to the
#    Delivery Order.
#
##############################################################################

class sale_order(osv.Model):
    _name = "sale.order"
    _inherit = "sale.order"


    ''' sale.order:_prepare_order_picking()
        -----------------------------------
        This method is extended to make sure the Sales Order reference is
        chained during the automated Delivery Order creation. This automated
        creation happens in the sale.order:__create_pickings_and_procurements()
        method.
        ----------------------------------------------------------------------- '''
    def _prepare_order_picking(self, cr, uid, order, context=None):

        result = super(sale_order,self)._prepare_order_picking(cr, uid, order, context)
        result['order_reference'] = order.client_order_ref
        return result





##############################################################################
#
#    procurement.order
#
#    This class extends procurement.order to chain the reference to the
#    Purchase Order.
#
##############################################################################


class procurement_order(osv.osv):
    _name = "procurement.order"
    _inherit = 'procurement.order'


    ''' procurement.order:create_procurement_purchase_order()
        -----------------------------------------------------
        This method is extended to make sure the Sales Order reference is
        chained during the automated Purchase Order creation.
        ------------------------------------------------------------------ '''
    def create_procurement_purchase_order(self, cr, uid, procurement, po_vals, line_vals, context=None):

        if procurement.origin:
            order_db = self.pool.get('sale.order')
            order_ids = order_db.search(cr, uid, [('name','=',procurement.origin)])
            if order_ids:
                for order in order_db.browse(cr, uid, order_ids, context=context):
                    if order.client_order_ref:
                        po_vals.update({'partner_ref': order.client_order_ref})

        return super(procurement_order,self).create_procurement_purchase_order(cr, uid, procurement, po_vals, line_vals, context)











