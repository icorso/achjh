from datetime import timedelta

from constants import EventType
from db import DbSession
from db_tables import OpenTransaction
from reporting.data import *
from reporting.helper import TransactionsHelper
from reporting.response import ACHJHResponse
from utils import rand_num


def reporting(request):
    events = []
    db = DbSession()
    helper = TransactionsHelper()

    for tx in helper.find_no_events_transactions():
        events_set = []

        # processing refunds (child) without events
        if tx.originaltransactionid and helper.is_ach_transaction(tx.originaltransactionid):  # refunds
            events_set = refund_set(tx.uniqueref, tx.rrn)

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
        elif '.57' in str(tx.amount):  # approved than charged back
            events_set = charged_back_set(tx.uniqueref, tx.rrn)
        elif '.58' in str(tx.amount):  # the "processed" event is duplicated
            events_set = duplicated_events_set(tx.uniqueref, tx.rrn)
        elif '.60' in str(tx.amount):  # return code R01
            events_set = [r01(tx.uniqueref, tx.rrn)]
        elif '.61' in str(tx.amount):  # return code R02
            events_set = [r02(tx.uniqueref, tx.rrn)]
        elif '.62' in str(tx.amount):  # return code R30
            events_set = [r30(tx.uniqueref, tx.rrn)]
        elif '.70' in str(tx.amount):  # return Unauthorized
            events_set = [unauthorized(tx.uniqueref, tx.rrn)]
        elif '.71' in str(tx.amount):  # return Processing error
            events_set = processing_error_set(tx.uniqueref, tx.rrn)
        elif '.72' in str(tx.amount):  # return Notice of change
            events_set = notice_of_change_set(tx.uniqueref, tx.rrn)
        elif '.73' in str(tx.amount):  # return Notice of change declined
            events_set = notice_of_change_declined_set(tx.uniqueref, tx.rrn)
        elif '.77' in str(tx.amount):  # return non-existing RRN
            events_set = [approved(tx.uniqueref, rand_num(10))]
        elif '.80' in str(tx.amount):  # return unknown event type
            events_set = [unknown_event_type(tx.uniqueref, tx.rrn)]
        else:                         # the rest txs become settled, see error in log: "not found ACH JH order with rrn"
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
                events.append(refunded(tx.uniqueref, tx.rrn, last_event.event_date_time + timedelta(hours=2)))
        else:
            if last_event.event_type == EventType.ORIGINATED.tid:
                events.append(refunded(tx.uniqueref, tx.rrn, last_event.event_date_time + timedelta(hours=1)))
            elif last_event.event_type == EventType.REFUNDED.tid:
                if float(tx.amount) == 16.52:
                    events.append(returned_nsf(tx.uniqueref, tx.rrn, last_event.event_date_time + timedelta(hours=2)))
                else:
                    events.append(settled(tx.uniqueref, tx.rrn, last_event.event_date_time + timedelta(hours=2)))
            elif last_event.event_type == EventType.SETTLED.tid and float(tx.amount) == 17.52:
                    events.append(returned_bad_account(tx.uniqueref, tx.rrn, last_event.event_date_time + timedelta(hours=2)))

    response = ACHJHResponse(events=events)
    return response
