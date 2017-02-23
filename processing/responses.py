import datetime

from lxml import etree

from spyne import ComplexModel, String, DateTime, Unicode, XmlData, Boolean, XmlAttribute
from spyne.util.xml import get_object_as_xml

from utils import wrap

DATETIME = '%Y-%m-%dT%H:%M:%S-06:00'
now = datetime.datetime.now()


class BaseResponse(ComplexModel):
    xmlns = XmlAttribute(Unicode, use='required')

    def __str__(self):
        self.xmlns = "https://ssl.selectpayment.com/PV"
        elt = get_object_as_xml(self, self.__class__)
        return wrap(etree.tostring(elt, pretty_print=True).decode('utf-8'))

    def encode(self):
        return [self.__str__().encode()]
    Data = XmlData(Unicode)


class BaseTransactionResult(BaseResponse):
    ReferenceNumber = String  # K08RKBLGBA3
    Success = Boolean  # true
    Error = Boolean  # false
    ResponseCode = String  # Success
    ActualDate = DateTime(format=DATETIME)  #2017-01-20T06:49:53.5971618-06:00
    ResponseMessage = String
    OriginatedAs = String  # ACH
    Data = XmlData(Unicode)


class AuthorizeTransactionResponse(BaseResponse):
    AuthorizeTransactionResult = BaseTransactionResult


class VoidTransactionResponse(BaseResponse):
    VoidTransactionResult = BaseTransactionResult


class RefundTransactionResponse(BaseResponse):
    RefundTransactionResult = BaseTransactionResult
