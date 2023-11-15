#!/usr/bin/env python3
"""
 Filtered Logging Module
"""
import re
from typing import List
import logging


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ filter datum """
    for item in fields:
        pattern = r'({}=)[A-Za-z0-9\/@?\.?\-*]+({})'.format(item, separator)
        repl = r'\1{}\2'.format(redaction)
        message = re.sub(pattern, repl, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        msg = record.getMessage()
        message = filter_datum(self.fields, self.REDACTION, msg,
                               self.SEPARATOR)
        record.msg = message
        return record.getMessage()
