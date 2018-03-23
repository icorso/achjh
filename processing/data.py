import datetime

from processing.responses import AuthorizeTransactionResponse, BaseTransactionResult, VoidTransactionResponse, \
    RefundTransactionResponse
from utils import rand_str

NOW = datetime.datetime.now()


DEFAULT_BASE_RESULT = BaseTransactionResult(
    ReferenceNumber=rand_str(11).upper(),
    Success=True,
    Error=False,
    ResponseCode='Success',
    ActualDate=NOW,
    ResponseMessage=None,
    OriginatedAs='ACH'
)

DEFAULT_AUTH = AuthorizeTransactionResponse(
    AuthorizeTransactionResult=BaseTransactionResult(
        ReferenceNumber=rand_str(11).upper(),
        Success=True,
        Error=False,
        ResponseCode='Success',
        ActualDate=NOW - datetime.timedelta(days=1),
        ResponseMessage=None,
        OriginatedAs='ACH'
    )
)

VELOCITY_COUNT = AuthorizeTransactionResponse(
    AuthorizeTransactionResult=BaseTransactionResult(
        ReferenceNumber=rand_str(11).upper(),
        Success=False,
        Error=False,
        ResponseCode='Velocity_Count',
        ActualDate=NOW,
        ResponseMessage='The following velocity exceptions occurred processing the transaction: Period_Count_Exception',
        OriginatedAs='ACH'
    )
)

UNSUFFICIENT_FUNDS = AuthorizeTransactionResponse(
    AuthorizeTransactionResult=BaseTransactionResult(
        ReferenceNumber=rand_str(11).upper(),
        Success=False,
        Error=False,
        ResponseCode='Insufficient_Funds',
        ActualDate=NOW,
        ResponseMessage='Insufficient_Funds Exception',
        OriginatedAs='ACH'
    )
)

DUPLICATE_TRANSACTION = AuthorizeTransactionResponse(
    AuthorizeTransactionResult=BaseTransactionResult(
        ReferenceNumber=rand_str(11).upper(),
        Success=False,
        Error=False,
        ResponseCode='Duplicate_Transaction',
        ActualDate=NOW, #'9999-12-31T23:59:59.9999999',
        ResponseMessage='This transaction is a duplicate of a previously run transaction. This transaction was ignored.',
        OriginatedAs='None'
    )
)

INVALID_ROUTING_NUM = AuthorizeTransactionResponse(
    AuthorizeTransactionResult=BaseTransactionResult(
        ReferenceNumber=rand_str(11).upper(),
        Success=False,
        Error=False,
        ResponseCode='Error_Unspecified',
        ActualDate=NOW,
        ResponseMessage="The RoutingNumber (%s) is not a valid Routing Number",
        OriginatedAs='ACH'
    )
)

DEFAULT_VOID = VoidTransactionResponse(
    VoidTransactionResult=DEFAULT_BASE_RESULT
)

DEFAULT_REFUND = RefundTransactionResponse(
    RefundTransactionResult=DEFAULT_BASE_RESULT
)

INVALID_REFUND = RefundTransactionResponse(
    RefundTransactionResult=BaseTransactionResult(
        ReferenceNumber=rand_str(11).upper(),
        Success=False,
        Error=False,
        ResponseCode='Error_Invalid_State',
        ActualDate=NOW,
        ResponseMessage='Transaction is in a state that cannot be refunded',
        OriginatedAs='ACH'
    )
)

