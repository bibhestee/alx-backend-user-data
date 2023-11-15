#!/usr/bin/env python3
"""
 Filtered Logging Module
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ filter datum """
    for item in fields:
        pattern = r'({}=)[A-Za-z0-9\/@?\.?]+({})'.format(item, separator)
        repl = r'\1{}\2'.format(redaction)
        message = re.sub(pattern, repl, message)
    return message
