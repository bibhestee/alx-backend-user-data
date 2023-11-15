#!/usr/bin/env python3
"""
 Filtered Logging Module
"""
import re
from typing import List
import logging
from os import getenv
import mysql.connector

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


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
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.setFormatter(RedactingFormatter(PII_FIELDS))
    logging.StreamHandler()
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ get database connector """
    db_name = getenv('PERSONAL_DATA_DB_NAME')
    usr = getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    pwd = getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    return mysql.connector.connect(user=usr, passwd=pwd, database=db_name,
                                   host=host)


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
