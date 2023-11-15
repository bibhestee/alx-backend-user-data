#!/usr/bin/env python3
"""
 Filtered Logging Module
"""
import re


def filter_datum(fields, redaction, message, separator):
    """ filter datum """
    for item in fields:
        pattern = r'({}=)[A-Za-z0-9\/@?\.?]+({})'.format(item, separator)
        repl = r'\1{}\2'.format(redaction)
        message = re.sub(pattern, repl, message)
    return message