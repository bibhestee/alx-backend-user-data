#!/usr/bin/env python3
"""
 Filtered Logging Module
"""
import re
from typing import List
import logging

PII_FIELDS = ('email', 'phone', 'ssn', 'password', 'ip')


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ filter datum """
    for item in fields:
        pattern = r'({}=)[A-Za-z0-9\/@?\.?\-*]+({})'.format(item, separator)
        repl = r'\1{}\2'.format(redaction)
        message = re.sub(pattern, repl, message)
    return message


def get_logger() -> logging.Logger:
    """ get a logger """
    logger = logging.getLogger('user_data')
    logging.basicConfig(level=logging.INFO, propagate=False,
                        stream=RedactingFormatter(PII_FIELDS))
    return logger


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        Methods:
            format: format the record with predefined formatter
        Attributes:
            REDACTION: redaction to format the record
            FORMAT: the format style
            SEPARATOR: the separator for the format style
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ format the record """
        msg = record.getMessage()
        record.msg = filter_datum(self.fields, self.REDACTION, msg,
                                  self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)
