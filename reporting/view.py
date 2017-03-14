from db import DbSession
from db_tables import OpenTransaction
from reporting.collector import txs_without_events, get_tx_by_id, has_events, get_gray_area_txs
from reporting.data import *
from reporting.response import ACHJHResponse


def reporting(request):
    events = []
    db = DbSession()

    for t in txs_without_events(tid=121):
        events_set = []

        if t.originaltransactionid:  # refunds
            events_set = refund_set(t.uniqueref, t.rrn)

            parent_tx = get_tx_by_id(t.originaltransactionid)
            parent_events = has_events(parent_tx.id)
            if len(parent_events) > 1:  # if any event exists, add refunded event as the last one
                last_event_date = parent_events[len(parent_events) - 1].event_date_time
                events_set.append(refunded(parent_tx.uniqueref, parent_tx.rrn,
                                           at=last_event_date + datetime.timedelta(hours=1)))
            else:  # if there are no events then add both approved and refunded events
                tx_date = parent_tx.txndate
                events_set.append(approved(parent_tx.uniqueref, parent_tx.rrn, at=tx_date + datetime.timedelta(hours=1)))
                events_set.append(refunded(parent_tx.uniqueref, parent_tx.rrn, at=tx_date + datetime.timedelta(hours=2)))
        elif '.50' in str(t.amount):  # approved, .90 amount is for gray area
            events_set = [approved(t.uniqueref, t.rrn, now - datetime.timedelta(days=1))]
        elif '.51' in str(t.amount):  # processed
            events_set = processed_set(t.uniqueref, t.rrn)
        elif '.52' in str(t.amount):  # originated
            events_set = originated_set(t.uniqueref, t.rrn)
        elif '.53' in str(t.amount):  # returned nsf
            events_set = returned_nsf_set(t.uniqueref, t.rrn)
        elif '.54' in str(t.amount):  # sent to collection
            events_set = sent_to_collection_set(t.uniqueref, t.rrn)
        elif '.55' in str(t.amount):  # returned bad account
            events_set = returned_bad_account_set(t.uniqueref, t.rrn)
        elif '.56' in str(t.amount):  # collection failed
            events_set = collection_failed_set(t.uniqueref, t.rrn)
        elif '.60' in str(t.amount):  # return code R01
            events_set = [r01(t.uniqueref, t.rrn)]
        elif '.61' in str(t.amount):  # return code R02
            events_set = [r02(t.uniqueref, t.rrn)]
        else:                         # the rest txs become settled
            events_set = settled_set(t.uniqueref, t.rrn)

        events.extend(events_set)

        db.update(OpenTransaction, OpenTransaction.id == t.id, {'txndate': events_set[0].EventDateTime})

    for t in get_gray_area_txs():  # gray area transactions which amount contains .90
        events.append(collection_failed(tn=t.uniqueref, rn=t.rrn))

    response = ACHJHResponse()
    response.events = events
    # tnx = get_open_tnx()
    # response = SETTLED.with_tn(tnx.uniqueref).with_rn(tnx.rrn).build()
    return response
