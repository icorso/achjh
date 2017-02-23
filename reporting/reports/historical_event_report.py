from spyne import ComplexModel, String, Int, DateTime, Unicode, XmlData, Array

from utils import DATETIME_PATTERN


class WSEventReport(ComplexModel):
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
    GetHistoricalEventReportResult = Array(WSEventReport)


