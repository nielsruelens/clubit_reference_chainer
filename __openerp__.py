{
    'name': 'clubit_reference_chainer',
    'version': '1.0',
    'category': 'Sales, Warehouse, Accounting',
    'description': "This module will make sure the reference entered in the Sale Order is chained all the way to the Delivery Order and the Customer Invoice.",
    'author': 'Niels Ruelens',
    'website': 'http://clubit.be',
    'summary': 'This module will make sure the reference entered in the Sale Order is chained all the way to the Delivery Order and the Customer Invoice.',
    'sequence': 9,
    'depends': [
        'account',
        'sale_stock',
        'purchase',
        'stock',
    ],
    'data': [
        'reference_view.xml',
    ],
    'demo': [
    ],
    'test': [
    ],
    'css': [
    ],
    'images': [
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}