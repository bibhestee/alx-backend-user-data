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
        pattern = r'({}=)[^;]+({})'.format(item, separator)
        repl = r'\1{}\2'.format(redaction)
        message = re.sub(pattern, repl, message)
    return message


def get_logger() -> logging.Logger:
    """ get a logger """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream = logging.StreamHandler()
    stream.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ get database connector """
    db = getenv('PERSONAL_DATA_DB_NAME')
    usr = getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    pwd = getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    return mysql.connector.connection.MySQLConnection(user=usr, password=pwd,
                                                      host=host, database=db)


def main():
    """ main function to connect to db and perform query of data """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    logger = get_logger()
    for row in cursor:
        n, e, ph, ssn, pa, ip, ll, ua = row
        msg = f'name={n};email={e};phone={ph};ssn={ssn};'
        msg += f'password={pa};ip={ip};last_login={ll};user_agent={ua}'
        logger.info(msg)
    cursor.close()
    db.close()


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


if __name__ == "__main__":
    main()
