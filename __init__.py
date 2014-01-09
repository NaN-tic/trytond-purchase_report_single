# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from .purchase import *


def register():
    Pool.register(
        PrintPurchaseWarning,
        module='purchase_report_single', type_='model')
    Pool.register(
        PrintPurchase,
        module='purchase_report_single', type_='wizard')
    Pool.register(
        PurchaseReport,
        module='purchase_report_single', type_='report')
