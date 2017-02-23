from lxml import objectify

from reporting.data import VOIDED
from utils import unwrap


def reporting(request):
    request = objectify.fromstring(unwrap(request))

    tn = 'BJGI0317N0'
    rn = 'OGWQKCWESFG'

    # response = SETTLED.with_tn(tn).with_rn(rn).build()
    response = VOIDED.with_tn(tn).with_rn(rn).build()
    # response = APPROVED.with_tn(tn).with_rn(rn).build()
    # response = REFUND.with_tn(tn).with_rn(rn).build()
    # response = FULL_REFUND.with_tn(tn).with_rn(rn).build()
    # response = COLLECTED.with_tn(tn).with_rn(rn).build()
    # response = BAD_ACCOUNT.with_tn(tn).with_rn(rn).build()
    # response = RETURNED_NSF.with_tn(tn).with_rn(rn).build()
    return response

