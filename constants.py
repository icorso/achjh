from enum import Enum

from utils import datetime_formatted

TRANSACTION_DATETIME = datetime_formatted('2001-01-01T00:00:00')


class SettlementStatus(Enum):
    CHARGED_BACK = ("Charged Back", 7)
    NO_SETTLEMENT_NEEDED = ("No Settlement Needed", 1)
    PENDING = ("Originated / Settlement Pending", 4)
    SETTLED = ("Settled", 6)
    TO_BE_ORIGINATED = ("To Be Originated", 2)
    ORIGINATING = ("Originating", 3)

    def __init__(self, status, sid):
        self.status = status
        self.sid = sid

    def __str__(self):
        return str(self.status)

    def status(self):
        return str(self.status)

    def sid(self):
        return str(self.sid)


class Status(Enum):
    PENDING = 1
    READY = 2
    VOID = 3
    DECLINED = 4
    COMPLETE = 5
    REFERRAL = 6
    PICKUP = 7
    REVERSAL = 8
    SENT = 9
    ADMIN = 10
    EXPIRED = 11
    IN_PROGRESS = 12

    def __init__(self, tid):
        self.tid = tid

    def __str__(self):
        return str(self.name)

    def tid(self):
        return str(self.tid)


class TransactionStatus(Enum):
    APPROVED = ("Approved", 2)
    COLLECTED = ("Collected", 6)
    CLOSED_ACCOUNT = ("Invalid / Closed Account", 15)
    DECLINED = ("Declined", 1)
    DISPUTED = ("Disputed", 13)
    ERROR = ("Error", 3)
    IN_COLLECTION = ("In Collection", 10)
    PROCESSED = ("Processed", 5)
    UNCOLLECTED_NSF = ("Uncollected NSF", 14)
    VOIDED = ("Voided", 4)

    def __init__(self, status, tid):
        self.status = status
        self.tid = tid

    def __str__(self):
        return str(self.status)

    def status(self):
        return str(self.status)

    def tid(self):
        return str(self.tid)


class EventType(Enum):
    APPROVED = ("Approved", 2)
    BAD_ACCOUNT = ("Returned Bad Account", 17)
    CAPTURED = ("Captured", 5)
    COLLECTION_FAILED = ("Collection Failed", 10)
    COLLECTED = ("Collected", 9)
    DECLINED = ("Declined", 1)
    DISPUTED = ("Disputed", 15)
    ORIGINATED = ("Originated", 11)
    PROCESSED = ("Processed", 8)
    PROCESSING_ERROR = ("Processing Error", 3)
    REFUNDED = ("Refunded", 6)
    RETURNED_NSF = ("Returned NSF", 16)
    SENT_TO_COLLECTION = ("Sent To Collection", 14)
    RETURNED_BAD_ACCOUNT = ("Returned Bad Account", 17)
    SETTLED = ("Settled", 12)
    VOIDED = ("Voided", 4)
    UNAUTHORIZED = ("Unauthorized", 21)
    NOTICE_OF_CHANGE = ("Notice Of Change", 19)

    def __init__(self, status, tid):
        self.status = status
        self.tid = tid

    def __str__(self):
        return str(self.status)

    def status(self):
        return str(self.status)

    def tid(self):  # enum AchJhEventTypeEnum index
        return str(self.tid)

