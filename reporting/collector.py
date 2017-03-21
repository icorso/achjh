from sqlalchemy import and_

from db import DbSession
from db_tables import OpenTransaction, AchjhTransactionStateHistory, ClosedTransaction, AchjhTransaction
from logger import log

db = DbSession()


def get_open_tnx():
    uniqref = 'FJ9P6JO99M'
    return db.query_first(OpenTransaction, OpenTransaction.uniqueref == uniqref)


def txs_without_events(terminal_id=None):
    txs = []
    txs_filter = [OpenTransaction.responsecode != 'D', OpenTransaction.cardtype == 26]
    if terminal_id:
        txs_filter.append(OpenTransaction.terminalid == terminal_id)
    for tx in db.query_all(OpenTransaction, and_(*txs_filter)):
        if len(has_events(tx.id)) == 0:
            txs.append(tx)

    for t in txs:  # exclude parent refund txs
        opened_tx = list(filter(lambda OpenTransaction: OpenTransaction.id == t.originaltransactionid, txs))
        if t.originaltransactionid and len(opened_tx) > 0:
            txs.remove(opened_tx[0])

    log.info("Collected '" + str(len(txs)) + "' transactions without events.")
    return txs


def get_tx_by_id(tx_id):
    tx = db.query_first(OpenTransaction, OpenTransaction.id == tx_id)
    if tx is not None:
        return tx
    else:
        return db.query_first(ClosedTransaction, ClosedTransaction.id == tx_id)


def get_gray_area_txs():
    txs = []
    for t in db.query_all(ClosedTransaction, ClosedTransaction.amount.contains('.90')):
        if db.query_first(AchjhTransaction, and_(AchjhTransaction.gray_area == 0, AchjhTransaction.id == t.id)):
            txs.append(t)
    return txs


def has_events(tx_id):
    return db.query_all(AchjhTransactionStateHistory, AchjhTransactionStateHistory.transaction_id == tx_id)
