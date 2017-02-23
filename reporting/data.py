import datetime

from constants import EventType as Et
from constants import SettlementStatus as Ss
from constants import TransactionStatus as Ts
from reporting.response import WSEventReport, ACHJHResponse

now = (datetime.datetime.now()).replace(hour=0, minute=0, second=0)

VOIDED = ACHJHResponse().with_event(WSEventReport(
        EventType=Et.APPROVED.status,
        TransactionStatus=Ts.VOIDED.status,
        SettlementStatus=Ss.NO_SETTLEMENT_NEEDED.status,
        EventDateTime=now - datetime.timedelta(minutes=5))
    ).with_event(WSEventReport(
        EventType=Et.VOIDED.status,
        TransactionStatus=Ts.VOIDED.status,
        SettlementStatus=Ss.NO_SETTLEMENT_NEEDED.status,
        EventDateTime=now - datetime.timedelta(minutes=3))
    )

SETTLED = ACHJHResponse().with_event(WSEventReport(
        EventType=Et.APPROVED.status,
        TransactionStatus=Ts.APPROVED.status,
        SettlementStatus=Ss.TO_BE_ORIGINATED.status,
        EventDateTime=now - datetime.timedelta(days=9, hours=22))
    ).with_event(WSEventReport(
        EventType=Et.PROCESSED.status,
        TransactionStatus=Ts.PROCESSED.status,
        SettlementStatus=Ss.TO_BE_ORIGINATED.status,
        EventDateTime=now - datetime.timedelta(days=9, hours=20))
    ).with_event(WSEventReport(
        EventType=Et.ORIGINATED.status,
        TransactionStatus=Ts.PROCESSED.status,
        SettlementStatus=Ss.PENDING.status,
        EventDateTime=now - datetime.timedelta(days=9))
    ).with_event(WSEventReport(
        EventType=Et.SETTLED.status,
        TransactionStatus=Ts.PROCESSED.status,
        SettlementStatus=Ss.SETTLED.status,
        EventDateTime=now - datetime.timedelta(days=2))
)

BAD_ACCOUNT = ACHJHResponse().with_event(WSEventReport(
        EventType=Et.APPROVED.status,
        TransactionStatus=Ts.APPROVED.status,
        SettlementStatus=Ss.TO_BE_ORIGINATED.status,
        EventDateTime=now - datetime.timedelta(days=6, hours=22))
    ).with_event(WSEventReport(  # Processed
        EventType=Et.PROCESSED.status,
        TransactionStatus=Ts.PROCESSED.status,
        SettlementStatus=Ss.TO_BE_ORIGINATED.status,
        EventDateTime=now - datetime.timedelta(days=6, hours=20))
    ).with_event(WSEventReport(  # Originated
        EventType=Et.ORIGINATED.status,
        TransactionStatus=Ts.PROCESSED.status,
        SettlementStatus=Ss.PENDING.status,
        EventDateTime=now - datetime.timedelta(days=6, hours=4))
    ).with_event(WSEventReport(  # Settled
        EventType=Et.SETTLED.status,
        TransactionStatus=Ts.PROCESSED.status,
        SettlementStatus=Ss.SETTLED.status,
        EventDateTime=now - datetime.timedelta(days=4))
    ).with_event(WSEventReport(
        EventType=Et.BAD_ACCOUNT.status,
        TransactionStatus=Ts.CLOSED_ACCOUNT.status,
        SettlementStatus=Ss.CHARGED_BACK.status,
        EventDateTime=now - datetime.timedelta(days=3, hours=14)
    ))

APPROVED = ACHJHResponse().with_event(WSEventReport(
        EventType=Et.APPROVED.status,
        TransactionStatus=Ts.APPROVED.status,
        SettlementStatus=Ss.TO_BE_ORIGINATED.status,
        EventDateTime=now - datetime.timedelta(days=3, hours=6))
    ).with_event(WSEventReport(
        EventType=Et.PROCESSED.status,
        TransactionStatus=Ts.PROCESSED.status,
        SettlementStatus=Ss.TO_BE_ORIGINATED.status,
        EventDateTime=now - datetime.timedelta(days=2, hours=22))
    ).with_event(WSEventReport(
        EventType=Et.ORIGINATED.status,
        TransactionStatus=Ts.PROCESSED.status,
        SettlementStatus=Ss.PENDING.status,
        EventDateTime=now - datetime.timedelta(days=1, hours=16))
    ).with_event(WSEventReport(
        EventType=Et.SETTLED.status,
        TransactionStatus=Ts.PROCESSED.status,
        SettlementStatus=Ss.SETTLED.status,
        EventDateTime=now - datetime.timedelta(days=1, hours=15, minutes=59))
    )

COLLECTED = ACHJHResponse().with_event(WSEventReport(
        EventType=Et.APPROVED.status,
        TransactionStatus=Ts.APPROVED.status,
        SettlementStatus=Ss.TO_BE_ORIGINATED.status,
        EventDateTime=now - datetime.timedelta(days=9, hours=22))
    ).with_event(WSEventReport(  # Processed
        EventType=Et.PROCESSED.status,
        TransactionStatus=Ts.PROCESSED.status,
        SettlementStatus=Ss.TO_BE_ORIGINATED.status,
        EventDateTime=now - datetime.timedelta(days=9, hours=20))
    ).with_event(WSEventReport(
        EventType=Et.ORIGINATED.status,
        TransactionStatus=Ts.PROCESSED.status,
        SettlementStatus=Ss.PENDING.status,
        EventDateTime=now - datetime.timedelta(days=9))
    ).with_event(WSEventReport(
        EventType=Et.SETTLED.status,
        TransactionStatus=Ts.PROCESSED.status,
        SettlementStatus=Ss.SETTLED.status,
        EventDateTime=now - datetime.timedelta(days=8))
    ).with_event(WSEventReport(
        EventType=Et.RETURNED_NSF.status,
        TransactionStatus=Ts.UNCOLLECTED_NSF.status,
        SettlementStatus=Ss.CHARGED_BACK.status,
        EventDateTime=now - datetime.timedelta(days=8, hours=10))
    ).with_event(WSEventReport(
        EventType=Et.SENT_TO_COLLECTION.status,
        TransactionStatus=Ts.IN_COLLECTION.status,
        SettlementStatus=Ss.CHARGED_BACK.status,
        EventDateTime=now - datetime.timedelta(days=4, hours=22))
    ).with_event(WSEventReport(
        EventType=Et.COLLECTION_FAILED.status,
        TransactionStatus=Ts.UNCOLLECTED_NSF.status,
        SettlementStatus=Ss.CHARGED_BACK.status,
        EventDateTime=now - datetime.timedelta(days=3, hours=22))
    ).with_event(WSEventReport(
        EventType=Et.COLLECTED.status,
        TransactionStatus=Ts.COLLECTED.status,
        SettlementStatus=Ss.CHARGED_BACK.status,
        EventDateTime=now - datetime.timedelta(days=2, hours=22))
    )

RETURNED_NSF = ACHJHResponse().with_event(WSEventReport(
        EventType=Et.APPROVED.status,
        TransactionStatus=Ts.APPROVED.status,
        SettlementStatus=Ss.TO_BE_ORIGINATED.status,
        EventDateTime=now - datetime.timedelta(days=9, hours=22))
    ).with_event(WSEventReport(
        EventType=Et.PROCESSED.status,
        TransactionStatus=Ts.PROCESSED.status,
        SettlementStatus=Ss.TO_BE_ORIGINATED.status,
        EventDateTime=now - datetime.timedelta(days=9, hours=20))
    ).with_event(WSEventReport(
        EventType=Et.ORIGINATED.status,
        TransactionStatus=Ts.PROCESSED.status,
        SettlementStatus=Ss.PENDING.status,
        EventDateTime=now - datetime.timedelta(days=9))
    ).with_event(WSEventReport(
        EventType=Et.SETTLED.status,
        TransactionStatus=Ts.PROCESSED.status,
        SettlementStatus=Ss.SETTLED.status,
        EventDateTime=now - datetime.timedelta(days=8))
    ).with_event(WSEventReport(
        EventType=Et.RETURNED_NSF.status,
        TransactionStatus=Ts.UNCOLLECTED_NSF.status,
        SettlementStatus=Ss.CHARGED_BACK.status,
        EventDateTime=now - datetime.timedelta(days=5, hours=4)))

REFUNDED = ACHJHResponse().with_event(WSEventReport(  # Approved
        EventType=Et.APPROVED.status,
        TransactionStatus=Ts.APPROVED.status,
        SettlementStatus=Ss.TO_BE_ORIGINATED.status,
        EventDateTime=now - datetime.timedelta(days=9, hours=22))
    ).with_event(WSEventReport(  # Processed
        EventType=Et.PROCESSED.status,
        TransactionStatus=Ts.PROCESSED.status,
        SettlementStatus=Ss.TO_BE_ORIGINATED.status,
        EventDateTime=now - datetime.timedelta(days=9, hours=20))
    ).with_event(WSEventReport(  # Originated
        EventType=Et.ORIGINATED.status,
        TransactionStatus=Ts.PROCESSED.status,
        SettlementStatus=Ss.PENDING.status,
        EventDateTime=now - datetime.timedelta(days=9))
    ).with_event(WSEventReport(  # Settled
        EventType=Et.SETTLED.status,
        TransactionStatus=Ts.PROCESSED.status,
        SettlementStatus=Ss.SETTLED.status,
        EventDateTime=now - datetime.timedelta(days=8))
    ).with_event(WSEventReport(
        EventType=Et.REFUNDED.status,
        TransactionStatus=Ts.PROCESSED.status,
        SettlementStatus=Ss.SETTLED.status,
        EventDateTime=now - datetime.timedelta(days=2, hours=5)))

REFUND = ACHJHResponse().with_event(WSEventReport(
        EventType=Et.APPROVED.status,
        TransactionStatus=Ts.PROCESSED.status,
        SettlementStatus=Ss.PENDING.status,
        EventDateTime=now - datetime.timedelta(days=2, hours=5))
    ).with_event(WSEventReport(
        EventType=Et.PROCESSED.status,
        TransactionStatus=Ts.PROCESSED.status,
        SettlementStatus=Ss.PENDING.status,
        EventDateTime=now - datetime.timedelta(days=1, hours=4))
    ).with_event(WSEventReport(
        EventType=Et.ORIGINATED.status,
        TransactionStatus=Ts.PROCESSED.status,
        SettlementStatus=Ss.PENDING.status,
        EventDateTime=now - datetime.timedelta(days=1))
    ).with_event(WSEventReport(
        EventType=Et.SETTLED.status,
        TransactionStatus=Ts.PROCESSED.status,
        SettlementStatus=Ss.PENDING.status,
        EventDateTime=now - datetime.timedelta(days=1)))

FULL_REFUND = ACHJHResponse().with_event(WSEventReport(
        EventType=Et.APPROVED.status,
        TransactionStatus=Ts.APPROVED.status,
        SettlementStatus=Ss.TO_BE_ORIGINATED.status,
        EventDateTime=now - datetime.timedelta(days=9, hours=22))
    ).with_event(WSEventReport(  # Processed
        EventType=Et.PROCESSED.status,
        TransactionStatus=Ts.PROCESSED.status,
        SettlementStatus=Ss.TO_BE_ORIGINATED.status,
        EventDateTime=now - datetime.timedelta(days=9, hours=20))
    ).with_event(WSEventReport(  # Originated
        EventType=Et.ORIGINATED.status,
        TransactionStatus=Ts.PROCESSED.status,
        SettlementStatus=Ss.PENDING.status,
        EventDateTime=now - datetime.timedelta(days=9))
    ).with_event(WSEventReport(  # Settled
        EventType=Et.SETTLED.status,
        TransactionStatus=Ts.PROCESSED.status,
        SettlementStatus=Ss.SETTLED.status,
        EventDateTime=now - datetime.timedelta(days=8))
    ).with_event(WSEventReport(
        EventType=Et.REFUNDED.status,
        TransactionStatus=Ts.PROCESSED.status,
        SettlementStatus=Ss.SETTLED.status,
        EventDateTime=now - datetime.timedelta(days=2, hours=5))
    ).with_event(WSEventReport(
        ReferenceNumber='HNNAXGAKBZS',
        EventType=Et.APPROVED.status,
        TransactionStatus=Ts.PROCESSED.status,
        SettlementStatus=Ss.PENDING.status,
        EventDateTime=now - datetime.timedelta(days=2, hours=5))
    ).with_event(WSEventReport(
        ReferenceNumber='HNNAXGAKBZS',
        EventType=Et.PROCESSED.status,
        TransactionStatus=Ts.PROCESSED.status,
        SettlementStatus=Ss.PENDING.status,
        EventDateTime=now - datetime.timedelta(days=1, hours=4))
    ).with_event(WSEventReport(
        ReferenceNumber='HNNAXGAKBZS',
        EventType=Et.ORIGINATED.status,
        TransactionStatus=Ts.PROCESSED.status,
        SettlementStatus=Ss.PENDING.status,
        EventDateTime=now - datetime.timedelta(days=1))
    ).with_event(WSEventReport(
        ReferenceNumber='HNNAXGAKBZS',
        EventType=Et.SETTLED.status,
        TransactionStatus=Ts.PROCESSED.status,
        SettlementStatus=Ss.PENDING.status,
        EventDateTime=now - datetime.timedelta(days=1)))
