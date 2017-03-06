from sqlalchemy import Column, Integer, String
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AchjhTransaction(Base):
    __tablename__ = 'ach_jh_transaction'

    id = Column(Integer, primary_key=True)
    account_type = Column(Integer)
    sec_code = Column(Integer)
    check_number = Column(String)
    routing_number = Column(String)
    originated_as = Column(String)
    response_code = Column(Integer)
    response_message = Column(String)
    reinitiation = Column(Integer)
    event_last = Column(Integer)
    event_last_date = Column(DateTime)
    transaction_status_last = Column(Integer)
    settlement_status_last = Column(Integer)
    region = Column(String)
    city = Column(String)
    return_code = Column(String)
    gray_area = Column(Integer)
    terminal_id = Column(Integer)
    rrn = Column(String)
    reinitiation_first_date = Column(DateTime)
    reinitiation_second_date = Column(DateTime)
    dl_state = Column(String)
    dl_number = Column(String)

    def __repr__(self):
        return "<AchjhTransaction(id='%s', rrn='%s', routing_number='%s')>" % (self.id, self.rrn, self.routing_number)


class AchjhTransactionStateHistory(Base):
    __tablename__ = 'ach_jh_transaction_state_history'
    id = Column(Integer, primary_key=True)
    transaction_id = Column(Integer)
    event_date_time = Column(DateTime)
    event_type = Column(Integer)
    transaction_status = Column(Integer)
    settlement_status = Column(Integer)


class OpenTransaction(Base):
    __tablename__ = 'open_transaction'

    id = Column(Integer, primary_key=True)
    terminalid = Column(Integer)
    txndate = Column(DateTime)
    status = Column(Integer)
    amount = Column(Float)
    cardholdername = Column(String)
    orderid = Column(String)
    description = Column(String)
    responsecode = Column(String)
    responsetext = Column(String)
    originaltransactionid = Column(String)
    approvalcode = Column(String)
    uniqueref = Column(String)
    rrn = Column(String)

    def __repr__(self):
        return "<OpenTransaction(id='%s', rrn='%s', uniqueref='%s')>" % (self.id, self.rrn, self.uniqueref)


class ClosedTransaction(Base):
    __tablename__ = 'closed_transaction'

    id = Column(Integer, primary_key=True)
    terminalid = Column(Integer)
    txndate = Column(DateTime)
    status = Column(Integer)
    amount = Column(Float)
    cardholdername = Column(String)
    orderid = Column(String)
    description = Column(String)
    responsecode = Column(String)
    responsetext = Column(String)
    originaltransactionid = Column(String)
    approvalcode = Column(String)
    uniqueref = Column(String)
    rrn = Column(String)

    def __repr__(self):
        return "<ClosedTransaction(id='%s', rrn='%s', uniqueref='%s')>" % (self.id, self.rrn, self.uniqueref)
