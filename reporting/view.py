from constants import EventType
from db import DbSession
from db_tables import OpenTransaction
from reporting.data import *
from reporting.helper import TransactionsHelper
from reporting.response import ACHJHResponse


def reporting(request):
    events = []
    db = DbSession()
    helper = TransactionsHelper()

    for tx in helper.find_no_events_transactions():
        events_set = []

        # processing refunds (child) without events
        if tx.originaltransactionid and helper.is_ach_transaction(tx.originaltransactionid):  # refunds
            events_set = refund_set(tx.uniqueref, tx.rrn)

            parent_tx = helper.find_transaction(tx.originaltransactionid)
            tx_date = parent_tx.txndate
            events_set.append(approved(parent_tx.uniqueref, parent_tx.rrn, at=tx_date + datetime.timedelta(hours=1)))
            events_set.append(refunded(parent_tx.uniqueref, parent_tx.rrn, at=tx_date + datetime.timedelta(hours=2)))

        elif '.50' in str(tx.amount):  # approved
            events_set = [approved(tx.uniqueref, tx.rrn, NOW - datetime.timedelta(days=1))]
        elif '.51' in str(tx.amount):  # processed
            events_set = processed_set(tx.uniqueref, tx.rrn)
        elif '.52' in str(tx.amount):  # originated
            events_set = originated_set(tx.uniqueref, tx.rrn)
        elif '.53' in str(tx.amount):  # returned nsf
            events_set = returned_nsf_set(tx.uniqueref, tx.rrn)
        elif '.54' in str(tx.amount):  # sent to collection
            events_set = sent_to_collection_set(tx.uniqueref, tx.rrn)
        elif '.55' in str(tx.amount):  # returned bad account
            events_set = returned_bad_account_set(tx.uniqueref, tx.rrn)
        elif '.56' in str(tx.amount):  # collection failed
            events_set = collection_failed_set(tx.uniqueref, tx.rrn)
        elif '.60' in str(tx.amount):  # return code R01
            events_set = [r01(tx.uniqueref, tx.rrn)]
        elif '.61' in str(tx.amount):  # return code R02
            events_set = [r02(tx.uniqueref, tx.rrn)]
        else:                         # the rest txs become settled
            events_set = settled_set(tx.uniqueref, tx.rrn)

        events.extend(events_set)

        db.update(OpenTransaction, OpenTransaction.id == tx.id, {'txndate': events_set[0].EventDateTime})

    for tx in helper.find_gray_area_transactions():  # gray area transactions which amount contains .90
        events.append(collection_failed(tn=tx.uniqueref, rn=tx.rrn))

    # processing original refunds
    for tx in helper.find_refunded_originals():
        parent_events = helper.find_transaction_events(tx.id)
        last_event = parent_events[len(parent_events) - 1]

        if helper.is_transaction_closed(tx.id):
            if last_event.event_type == EventType.SETTLED.tid:
                events.append(refunded(tx.uniqueref, tx.rrn, at=last_event.event_date_time + datetime.timedelta(hours=2)))
        else:
            if last_event.event_type == EventType.ORIGINATED.tid:
                events.append(refunded(tx.uniqueref, tx.rrn, at=last_event.event_date_time + datetime.timedelta(hours=1)))
            elif last_event.event_type == EventType.REFUNDED.tid:
                events.append(settled(tx.uniqueref, tx.rrn, at=last_event.event_date_time + datetime.timedelta(hours=2)))

    response = ACHJHResponse(events=events)
    return response
