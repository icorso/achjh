import datetime
from enum import Enum

from constants import EventType as Et
from constants import SettlementStatus as Ss
from constants import TransactionStatus as Ts
from db import DbSession
from db_tables import OpenTransaction
from reporting.collector import txs_without_events, get_tx_by_id, has_events, get_gray_area_txs
from reporting.reports.historical_event_report import WSEventReport
from reporting.response import ACHJHResponse

now = (datetime.datetime.now()).replace(hour=0, minute=0, second=0)


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
        elif '.50' in str(t.amount) or '.90' in str(t.amount):  # settled, .90 amount is for gray area
            events_set = settled_set(t.uniqueref, t.rrn)
        elif '.51' in str(t.amount):  # processed
            events_set = processed_set(t.uniqueref, t.rrn)
        elif '.52' in str(t.amount):  # originated
            events_set = originated_set(t.uniqueref, t.rrn)
        elif '.53' in str(t.amount):  # returned nsf
            events_set = returned_nsf_set(t.uniqueref, t.rrn)
        elif '.54' in str(t.amount):  # sent to collection
            events_set = sent_to_collection_set(t.uniqueref, t.rrn)
        elif '.55' in str(t.amount):  # sent to collection
            events_set = returned_bad_account_set(t.uniqueref, t.rrn)
        elif '.56' in str(t.amount):  # collection failed
            events_set = collection_failed_set(t.uniqueref, t.rrn)
        elif '.60' in str(t.amount):  # return code R01
            events_set = [r01(t.uniqueref, t.rrn)]
        elif '.61' in str(t.amount):  # return code R02
            events_set = [r02(t.uniqueref, t.rrn)]
        else:
            events_set = [approved(t.uniqueref, t.rrn, now - datetime.timedelta(days=1))]

        events.extend(events_set)

        db.update(OpenTransaction, OpenTransaction.id == t.id, {'txndate': events_set[0].EventDateTime})

    for t in get_gray_area_txs():  # gray area transactions
        events.append(collection_failed(tn=t.uniqueref, rn=t.rrn))

    response = ACHJHResponse()
    response.events = events
    # tnx = get_open_tnx()
    # response = SETTLED.with_tn(tnx.uniqueref).with_rn(tnx.rrn).build()
    return response


class EventDate(Enum):
    APPROVED = now - datetime.timedelta(days=9, hours=22)
    PROCESSED = now - datetime.timedelta(days=9, hours=20)
    ORIGINATED = now - datetime.timedelta(days=8)

    def __init__(self, date):
        self.date = date


def approved(tn, rn, at=EventDate.APPROVED.date):
    return WSEventReport(TransactionNumber=tn, ReferenceNumber=rn, EventType=Et.APPROVED.status, EventDateTime=at,
                         TransactionStatus=Ts.APPROVED.status, SettlementStatus=Ss.TO_BE_ORIGINATED.status)


def processed(tn, rn, at=EventDate.PROCESSED.date):
    return WSEventReport(EventType=Et.PROCESSED.status, TransactionNumber=tn, ReferenceNumber=rn, EventDateTime=at,
                         TransactionStatus=Ts.PROCESSED.status, SettlementStatus=Ss.TO_BE_ORIGINATED.status)


def originated(tn, rn, at=EventDate.ORIGINATED.date):
    return WSEventReport(TransactionNumber=tn, ReferenceNumber=rn, EventType=Et.ORIGINATED.status,
                         TransactionStatus=Ts.PROCESSED.status, SettlementStatus=Ss.PENDING.status, EventDateTime=at)


def settled(tn, rn, at=EventDate.ORIGINATED.date):
    return WSEventReport(TransactionNumber=tn, ReferenceNumber=rn, EventType=Et.SETTLED.status,
                         TransactionStatus=Ts.PROCESSED.status, SettlementStatus=Ss.SETTLED.status, EventDateTime=at)


def returned_nsf(tn, rn, at=now - datetime.timedelta(days=3)):
    return WSEventReport(TransactionNumber=tn, ReferenceNumber=rn, EventType=Et.RETURNED_NSF.status, EventDateTime=at,
                         TransactionStatus=Ts.UNCOLLECTED_NSF.status, SettlementStatus=Ss.CHARGED_BACK.status)


def sent_to_collection(tn, rn, at=now - datetime.timedelta(days=2)):
    return WSEventReport(TransactionNumber=tn, ReferenceNumber=rn, EventDateTime=at,
                         EventType=Et.SENT_TO_COLLECTION.status, TransactionStatus=Ts.IN_COLLECTION.status,
                         SettlementStatus=Ss.CHARGED_BACK.status)


def collection_failed(tn, rn, at=now):
    return WSEventReport(TransactionNumber=tn, ReferenceNumber=rn, EventDateTime=at,
                         EventType=Et.COLLECTION_FAILED.status, TransactionStatus=Ts.UNCOLLECTED_NSF.status,
                         SettlementStatus=Ss.CHARGED_BACK.status)


def returned_bad_account(tn, rn, at=now - datetime.timedelta(days=3)):
    return WSEventReport(TransactionNumber=tn, ReferenceNumber=rn, EventDateTime=at,
                         EventType=Et.RETURNED_BAD_ACCOUNT.status, TransactionStatus=Ts.CLOSED_ACCOUNT.status,
                         SettlementStatus=Ss.CHARGED_BACK.status)


def refunded(tn, rn, at=now - datetime.timedelta(days=2, hours=5)):
    return WSEventReport(TransactionNumber=tn, ReferenceNumber=rn, EventType=Et.REFUNDED.status,
                         TransactionStatus=Ts.PROCESSED.status, SettlementStatus=Ss.SETTLED.status, EventDateTime=at)


def r01(tn, rn, at=now - datetime.timedelta(days=1)):
    return WSEventReport(TransactionNumber=tn, ReferenceNumber=rn, EventType=Et.BAD_ACCOUNT.status, EventDateTime=at,
                         TransactionStatus=Ts.PROCESSED.status, SettlementStatus=Ss.NO_SETTLEMENT_NEEDED.status,
                         ReturnCode='R01')


def r02(tn, rn, at=now - datetime.timedelta(days=1)):
    return WSEventReport(TransactionNumber=tn, ReferenceNumber=rn, EventType=Et.BAD_ACCOUNT.status, EventDateTime=at,
                         TransactionStatus=Ts.CLOSED_ACCOUNT.status, SettlementStatus=Ss.NO_SETTLEMENT_NEEDED.status,
                         ReturnCode='R02')


def refund_set(tn, rn):
    return [WSEventReport(TransactionNumber=tn, ReferenceNumber=rn, EventType=Et.APPROVED.status,
                          TransactionStatus=Ts.PROCESSED.status, SettlementStatus=Ss.PENDING.status,
                          EventDateTime=now - datetime.timedelta(days=2, hours=5)),
            WSEventReport(TransactionNumber=tn, ReferenceNumber=rn, EventType=Et.PROCESSED.status,
                          TransactionStatus=Ts.PROCESSED.status, SettlementStatus=Ss.PENDING.status,
                          EventDateTime=now - datetime.timedelta(days=1, hours=4)),
            WSEventReport(TransactionNumber=tn, ReferenceNumber=rn, EventType=Et.ORIGINATED.status,
                          TransactionStatus=Ts.PROCESSED.status, SettlementStatus=Ss.PENDING.status,
                          EventDateTime=now - datetime.timedelta(days=1)),
            WSEventReport(TransactionNumber=tn, ReferenceNumber=rn, EventType=Et.SETTLED.status,
                          TransactionStatus=Ts.PROCESSED.status, SettlementStatus=Ss.PENDING.status,
                          EventDateTime=now - datetime.timedelta(days=1))]


def settled_set(tn, rn):
    return [approved(tn, rn), processed(tn, rn), originated(tn, rn), settled(tn, rn)]


def processed_set(tn, rn):
    return [approved(tn, rn), processed(tn, rn)]


def originated_set(tn, rn):
    return [approved(tn, rn), processed(tn, rn), originated(tn, rn)]


def returned_nsf_set(tn, rn):
    return [approved(tn, rn), processed(tn, rn), originated(tn, rn), settled(tn, rn), returned_nsf(tn, rn)]


def returned_bad_account_set(tn, rn):
    return [approved(tn, rn), processed(tn, rn), originated(tn, rn), settled(tn, rn), returned_bad_account(tn, rn)]


def sent_to_collection_set(tn, rn):
    return [approved(tn, rn), processed(tn, rn), originated(tn, rn), settled(tn, rn), returned_nsf(tn, rn),
            sent_to_collection(tn, rn)]


def collection_failed_set(tn, rn):
    return [approved(tn, rn), processed(tn, rn), originated(tn, rn), settled(tn, rn), sent_to_collection(tn, rn),
            collection_failed(tn, rn, at=now - datetime.timedelta(days=1))]
