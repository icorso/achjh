from lxml import objectify

from processing.data import DEFAULT_AUTH, VELOCITY_COUNT, UNSUFFICIENT_FUNDS, INVALID_ROUTING_NUM, DEFAULT_REFUND, NOW,\
    DEFAULT_VOID, INVALID_REFUND
from utils import unwrap, rand_str

bad_refund_state = "BADRFD"
wrong_routing_number = 'The RoutingNumber (%s) is not a valid Routing Number'


def processing(request):
    request = objectify.fromstring(unwrap(request))

    response = None
    if 'AuthorizeTransaction' in request.tag:
        response = DEFAULT_AUTH
        response.AuthorizeTransactionResult.ReferenceNumber = rand_str(11).upper()

        if '.01' in str(request.transaction.TotalAmount):  # Error_Invalid_State for refund
            response = DEFAULT_AUTH
            response.AuthorizeTransactionResult.ReferenceNumber = rand_str(6).upper() + bad_refund_state
        if '.02' in str(request.transaction.TotalAmount):
            response = VELOCITY_COUNT
        if '.03' in str(request.transaction.TotalAmount):
            response = UNSUFFICIENT_FUNDS
        if '.04' in str(request.transaction.TotalAmount):
            response = INVALID_ROUTING_NUM
            response.AuthorizeTransactionResult.ResponseMessage = wrong_routing_number % request.transaction.RoutingNumber

    if 'VoidTransaction' in request.tag:
        response = DEFAULT_VOID
        response.VoidTransactionResult.ReferenceNumber = str(request.originalReferenceNumber)
        response.VoidTransactionResult.ResponseMessage = None

    if 'RefundTransaction' in request.tag:
        response = DEFAULT_REFUND
        response.RefundTransactionResult.ReferenceNumber = rand_str(11).upper()
        response.RefundTransactionResult.ResponseMessage = "Transaction '%s' will be refunded on %s" \
                                                           % (request.originalReferenceNumber,
                                                              NOW.strftime('%A, %B  %d, %Y'))

        if str(request.originalReferenceNumber).endswith(bad_refund_state):
            response = INVALID_REFUND

    return response
