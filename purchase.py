# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelView
from trytond.pool import Pool, PoolMeta
from trytond.rpc import RPC
from trytond.transaction import Transaction
from trytond.wizard import (Wizard, StateView, StateTransition, StateAction,
    Button)

__all__ = ['PrintPurchaseWarning', 'PrintPurchase', 'PurchaseReport']
__metaclass__ = PoolMeta


class PrintPurchaseWarning(ModelView):
    '''Print Purchase Report Warning'''
    __name__ = 'purchase.print.warning'


class PrintPurchase(Wizard):
    'Print Purchase Report'
    __name__ = 'purchase.print'
    start = StateTransition()
    warning = StateView('purchase.print.warning',
        'purchase_report_single.print_warning_view_form', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Print', 'print_', 'tryton-print', default=True),
            ])
    print_ = StateAction('purchase.report_purchase')

    def transition_start(self):
        if len(Transaction().context['active_ids']) > 1:
            return 'warning'
        return 'print_'

    def do_print_(self, action):
        data = {}
        data['id'] = Transaction().context['active_ids'].pop()
        data['ids'] = [data['id']]
        return action, data

    def transition_print_(self):
        if Transaction().context['active_ids']:
            return 'print_'
        return 'end'


class PurchaseReport:
    __name__ = 'purchase.purchase'

    @classmethod
    def __setup__(cls):
        super(PurchaseReport, cls).__setup__()
        cls.__rpc__['execute'] = RPC(False)

    @classmethod
    def execute(cls, ids, data):
        Purchase = Pool().get('purchase.purchase')

        res = super(PurchaseReport, cls).execute(ids, data)
        if len(ids) > 1:
            res = (res[0], res[1], True, res[3])
        else:
            purchase = Purchase(ids[0])
            if purchase.reference:
                res = (res[0], res[1], res[2],
                    res[3] + ' - ' + purchase.reference)
        return res

    @classmethod
    def _get_records(cls, ids, model, data):
        with Transaction().set_context(language=False):
            return super(PurchaseReport, cls)._get_records(ids[:1], model,
                data)
