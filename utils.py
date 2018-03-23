import random
import string
from datetime import datetime

DATETIME_PATTERN = '%Y-%m-%dT%H:%M:%S'


def unwrap(xml):  # TODO
    header = u'''<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body>'''
    footer = u'''</soap:Body></soap:Envelope>'''
    xml = xml.replace(header, '')
    xml = xml.replace(footer, '')
    return xml


def wrap(xml):  # TODO
    header = u'''<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <soap:Header/><soap:Body>'''
    footer = u'''</soap:Body></soap:Envelope>'''
    return header + xml + footer


def randrus_str(length=10):
    valid_letters = 'АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя'
    return ''.join((random.choice(valid_letters) for i in range(length)))


def rand_str(length=10):
    return ''.join(random.sample(string.ascii_letters, length))


def rand_num(length=6):
    digits = '0123456789'
    return ''.join((random.choice(digits) for i in range(length)))


def datetime_formatted(date: str):
    return datetime.now().strptime(date, DATETIME_PATTERN)
