from spyne import ComplexModel, String, Int, DateTime, Unicode, XmlData, Array, XmlAttribute

from utils import DATETIME_PATTERN


class WSEventReport(ComplexModel):
    def tn(self, value):
        self.TransactionNumber = value

    def rn(self, value):
        self.ReferenceNumber = value

    TransactionStatus = String
    TransactionNumber = String
    ReferenceNumber = String
    TransactionDateTime = DateTime(format=DATETIME_PATTERN)
    TotalAmount = Int
    SettlementStatus = String
    OwnerAppReferenceId = Int
    ReturnCode = String
    EventDateTime = DateTime(format=DATETIME_PATTERN)
    EventType = String
    Data = XmlData(Unicode)


class GetHistoricalEventReportResponse(ComplexModel):
    xmlns = XmlAttribute(Unicode, use='required')
    GetHistoricalEventReportResult = Array(WSEventReport)


