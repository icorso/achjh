import datetime

from constants import EventType as Et
from constants import SettlementStatus as Ss
from constants import TransactionStatus as Ts
from reporting.reports.historical_event_report import WSEventReport
from utils import rand_str

NOW = (datetime.datetime.now()).replace(hour=0, minute=0, second=0)


def approved(tn, rn, at=NOW - datetime.timedelta(days=9, hours=22)):
    return WSEventReport(TransactionNumber=tn, ReferenceNumber=rn, EventType=Et.APPROVED.status, EventDateTime=at,
                         TransactionStatus=Ts.APPROVED.status, SettlementStatus=Ss.TO_BE_ORIGINATED.status)


def unknown_event_type(tn, rn, at=NOW + datetime.timedelta(minutes=1)):
    return WSEventReport(TransactionNumber=tn, ReferenceNumber=rn, EventType=rand_str(10), EventDateTime=at,
                         TransactionStatus=Ts.ERROR.status, SettlementStatus=Ss.NO_SETTLEMENT_NEEDED.status)


def processed(tn, rn, at=NOW - datetime.timedelta(days=9, hours=20)):
    return WSEventReport(EventType=Et.PROCESSED.status, TransactionNumber=tn, ReferenceNumber=rn, EventDateTime=at,
                         TransactionStatus=Ts.PROCESSED.status, SettlementStatus=Ss.TO_BE_ORIGINATED.status)


def originated(tn, rn, at=NOW - datetime.timedelta(days=8)):
    return WSEventReport(TransactionNumber=tn, ReferenceNumber=rn, EventType=Et.ORIGINATED.status,
                         TransactionStatus=Ts.PROCESSED.status, SettlementStatus=Ss.PENDING.status, EventDateTime=at)


def settled(tn, rn, at=NOW - datetime.timedelta(days=8)):
    return WSEventReport(TransactionNumber=tn, ReferenceNumber=rn, EventType=Et.SETTLED.status,
                         TransactionStatus=Ts.PROCESSED.status, SettlementStatus=Ss.SETTLED.status, EventDateTime=at)


def returned_nsf(tn, rn, at=NOW - datetime.timedelta(days=3)):
    return WSEventReport(TransactionNumber=tn, ReferenceNumber=rn, EventType=Et.RETURNED_NSF.status, EventDateTime=at,
                         TransactionStatus=Ts.UNCOLLECTED_NSF.status, SettlementStatus=Ss.CHARGED_BACK.status)


def sent_to_collection(tn, rn, at=NOW - datetime.timedelta(days=2)):
    return WSEventReport(TransactionNumber=tn, ReferenceNumber=rn, EventDateTime=at,
                         EventType=Et.SENT_TO_COLLECTION.status, TransactionStatus=Ts.IN_COLLECTION.status,
                         SettlementStatus=Ss.CHARGED_BACK.status)


def collection_failed(tn, rn, at=NOW):
    return WSEventReport(TransactionNumber=tn, ReferenceNumber=rn, EventDateTime=at,
                         EventType=Et.COLLECTION_FAILED.status, TransactionStatus=Ts.UNCOLLECTED_NSF.status,
                         SettlementStatus=Ss.CHARGED_BACK.status)


def returned_bad_account(tn, rn, at=NOW - datetime.timedelta(days=3)):
    return WSEventReport(TransactionNumber=tn, ReferenceNumber=rn, EventDateTime=at,
                         EventType=Et.RETURNED_BAD_ACCOUNT.status, TransactionStatus=Ts.CLOSED_ACCOUNT.status,
                         SettlementStatus=Ss.CHARGED_BACK.status)


def refunded(tn, rn, at=NOW - datetime.timedelta(days=2, hours=5)):
    return WSEventReport(TransactionNumber=tn, ReferenceNumber=rn, EventType=Et.REFUNDED.status,
                         TransactionStatus=Ts.PROCESSED.status, SettlementStatus=Ss.SETTLED.status, EventDateTime=at)


def r01(tn, rn, at=NOW - datetime.timedelta(days=1)):
    return WSEventReport(TransactionNumber=tn, ReferenceNumber=rn, EventType=Et.BAD_ACCOUNT.status, EventDateTime=at,
                         TransactionStatus=Ts.PROCESSED.status, SettlementStatus=Ss.NO_SETTLEMENT_NEEDED.status,
                         ReturnCode='R01')


def r02(tn, rn, at=NOW - datetime.timedelta(days=1)):
    return WSEventReport(TransactionNumber=tn, ReferenceNumber=rn, EventType=Et.BAD_ACCOUNT.status, EventDateTime=at,
                         TransactionStatus=Ts.CLOSED_ACCOUNT.status, SettlementStatus=Ss.NO_SETTLEMENT_NEEDED.status,
                         ReturnCode='R02')


def r30(tn, rn, at=NOW - datetime.timedelta(days=1)):
    return WSEventReport(TransactionNumber=tn, ReferenceNumber=rn, EventType=Et.BAD_ACCOUNT.status, EventDateTime=at,
                         TransactionStatus=Ts.CLOSED_ACCOUNT.status, SettlementStatus=Ss.NO_SETTLEMENT_NEEDED.status,
                         ReturnCode='R30')


def unauthorized(tn, rn, at=NOW - datetime.timedelta(days=1)):
    return WSEventReport(TransactionNumber=tn, ReferenceNumber=rn, EventType=Et.UNAUTHORIZED.status, EventDateTime=at,
                         TransactionStatus=Ts.ERROR.status, SettlementStatus=Ss.NO_SETTLEMENT_NEEDED.status)


def processing_error(tn, rn, at=NOW - datetime.timedelta(days=9)):
    return WSEventReport(TransactionNumber=tn, ReferenceNumber=rn, EventType=Et.PROCESSING_ERROR.status, EventDateTime=at,
                         TransactionStatus=Ts.ERROR.status, SettlementStatus=Ss.NO_SETTLEMENT_NEEDED.status)


def notice_of_change(tn, rn, at=NOW - datetime.timedelta(days=7)):
    return WSEventReport(TransactionNumber=tn, ReferenceNumber=rn, EventType=Et.NOTICE_OF_CHANGE.status, EventDateTime=at,
                         TransactionStatus=Ts.PROCESSED.status, SettlementStatus=Ss.SETTLED.status)


def notice_of_change_charged_back(tn, rn, at=NOW - datetime.timedelta(days=7)):
    return WSEventReport(TransactionNumber=tn, ReferenceNumber=rn, EventType=Et.NOTICE_OF_CHANGE.status, EventDateTime=at,
                         TransactionStatus=Ts.PROCESSED.status, SettlementStatus=Ss.CHARGED_BACK.status)


def charged_back(tn, rn, at=NOW - datetime.timedelta(days=1)):
    return WSEventReport(TransactionNumber=tn, ReferenceNumber=rn, EventType=Et.CHARGED_BACK.status, EventDateTime=at,
                         TransactionStatus=Ts.CLOSED_ACCOUNT.status, SettlementStatus=Ss.CHARGED_BACK.status)


def refund_set(tn, rn):
    return [WSEventReport(TransactionNumber=tn, ReferenceNumber=rn, EventType=Et.APPROVED.status,
                          TransactionStatus=Ts.PROCESSED.status, SettlementStatus=Ss.PENDING.status,
                          EventDateTime=NOW - datetime.timedelta(days=2, hours=5)),
            WSEventReport(TransactionNumber=tn, ReferenceNumber=rn, EventType=Et.PROCESSED.status,
                          TransactionStatus=Ts.PROCESSED.status, SettlementStatus=Ss.PENDING.status,
                          EventDateTime=NOW - datetime.timedelta(days=1, hours=4)),
            WSEventReport(TransactionNumber=tn, ReferenceNumber=rn, EventType=Et.ORIGINATED.status,
                          TransactionStatus=Ts.PROCESSED.status, SettlementStatus=Ss.PENDING.status,
                          EventDateTime=NOW - datetime.timedelta(days=1)),
            WSEventReport(TransactionNumber=tn, ReferenceNumber=rn, EventType=Et.SETTLED.status,
                          TransactionStatus=Ts.PROCESSED.status, SettlementStatus=Ss.PENDING.status,
                          EventDateTime=NOW - datetime.timedelta(days=1))]


def settled_set(tn, rn):
    return [approved(tn, rn), processed(tn, rn), originated(tn, rn), settled(tn, rn)]


def processed_set(tn, rn):
    return [approved(tn, rn), processed(tn, rn)]


def originated_set(tn, rn):
    return [approved(tn, rn), processed(tn, rn), originated(tn, rn)]


def duplicated_events_set(tn, rn):
    return [approved(tn, rn), processed(tn, rn), processed(tn, rn), originated(tn, rn)]


def returned_nsf_set(tn, rn):
    return [approved(tn, rn), processed(tn, rn), originated(tn, rn), settled(tn, rn), returned_nsf(tn, rn)]


def returned_bad_account_set(tn, rn):
    return [approved(tn, rn), processed(tn, rn), originated(tn, rn), settled(tn, rn), returned_bad_account(tn, rn)]


def sent_to_collection_set(tn, rn):
    return [approved(tn, rn), processed(tn, rn), originated(tn, rn), settled(tn, rn), returned_nsf(tn, rn),
            sent_to_collection(tn, rn)]


def collection_failed_set(tn, rn):
    return [approved(tn, rn), processed(tn, rn), originated(tn, rn), settled(tn, rn), sent_to_collection(tn, rn),
            collection_failed(tn, rn, at=NOW - datetime.timedelta(days=1))]


def processing_error_set(tn, rn):
    return [approved(tn, rn), processing_error(tn, rn)]


def notice_of_change_set(tn, rn):
    return [approved(tn, rn), processed(tn, rn), originated(tn, rn), originated(tn, rn), settled(tn, rn), notice_of_change(tn, rn)]


def notice_of_change_declined_set(tn, rn):
    return [approved(tn, rn), processed(tn, rn), originated(tn, rn), settled(tn, rn), notice_of_change_charged_back(tn, rn)]


def charged_back_set(tn, rn):
    return [approved(tn, rn), charged_back(tn, rn)]
