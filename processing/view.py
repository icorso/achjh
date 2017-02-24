from lxml import objectify

from processing.data import DEFAULT_AUTH, VELOCITY_COUNT, UNSUFFICIENT_FUNDS, INVALID_ROUTING_NUM, DEFAULT_REFUND, now,\
    DEFAULT_VOID, INVALID_REFUND
from utils import unwrap, rand_str

bad_refund_state = "BADRFD"


def processing(request):
    request = objectify.fromstring(unwrap(request))

    response = None
    if 'AuthorizeTransaction' in request.tag:
        response = DEFAULT_AUTH
        response.AuthorizeTransactionResult.ReferenceNumber = rand_str(11).upper()

        if '.01' in str(request.transaction.TotalAmount):  # Error_Invalid_State for refund
            response = DEFAULT_AUTH
            response.AuthorizeTransactionResult.ReferenceNumber = rand_str(5).upper() + bad_refund_state
        if '.11' in str(request.transaction.TotalAmount):
            response = VELOCITY_COUNT
        if '.21' in str(request.transaction.TotalAmount):
            response = UNSUFFICIENT_FUNDS
        if '.31' in str(request.transaction.TotalAmount):
            response = INVALID_ROUTING_NUM
            message = response.AuthorizeTransactionResult.ResponseMessage % request.transaction.RoutingNumber
            response.AuthorizeTransactionResult.ResponseMessage = message

    if 'VoidTransaction' in request.tag:
        response = DEFAULT_VOID
        response.VoidTransactionResult.ReferenceNumber = str(request.originalReferenceNumber)

    if 'RefundTransaction' in request.tag:
        response = DEFAULT_REFUND
        response.RefundTransactionResult.ReferenceNumber = rand_str(11).upper()
        response.RefundTransactionResult.ResponseMessage = "Transaction '%s' will be refunded on %s" \
                                                           % (request.originalReferenceNumber,
                                                              now.strftime('%A, %B  %d, %Y'))

        if str(request.originalReferenceNumber).endswith(bad_refund_state):
            response = INVALID_REFUND
    return response
