import random
import string
from datetime import datetime
from lxml import etree

DATETIME_PATTERN = '%Y-%m-%dT%H:%M:%S'


def unwrap(xml):  # TODO
    header = '''<?xml version='1.0' encoding='UTF-8'?><S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/" xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"><SOAP-ENV:Header/><S:Body>'''
    footer = '''</S:Body></S:Envelope>'''
    xml = xml.replace(header, '')
    xml = xml.replace(footer, '')
    return xml


def wrap(xml):  # TODO
    header = '''<?xml version='1.0' encoding='UTF-8'?><S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/" xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"><SOAP-ENV:Header/><S:Body>'''
    footer = '''</S:Body></S:Envelope>'''
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
