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

    Data = XmlData(Unicode)


class BaseTransactionResult(BaseResponse):
    ReferenceNumber = String
    Success = Boolean
    Error = Boolean
    ResponseCode = String
    ActualDate = DateTime(format=DATETIME)
    ResponseMessage = String
    OriginatedAs = String
    Data = XmlData(Unicode)


class AuthorizeTransactionResponse(BaseResponse):
    AuthorizeTransactionResult = BaseTransactionResult


class VoidTransactionResponse(BaseResponse):
    VoidTransactionResult = BaseTransactionResult


class RefundTransactionResponse(BaseResponse):
    RefundTransactionResult = BaseTransactionResult
