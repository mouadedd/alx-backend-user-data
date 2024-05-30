#!/usr/bin/env python3
""" personal data """
import os
import re
import logging
from typing import List, Tuple
import mysql.connector

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str],
                 redaction: str, message: str, separator: str) -> str:
    """filter a fiels content with a message"""
    for field in fields:
        pattern = r'({0}=)[^{1}]*({1})'.format(field, separator)
        message = re.sub(pattern, r'\1{}\2'.format(redaction), message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """log formatter"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """accept a list strings"""
        login = super(RedactingFormatter, self).format(record=record)
        return filter_datum(self.fields, self.REDACTION, login, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """Create logger"""
    log = logging.getLogger('user_data')
    log.setLevel(logging.INFO)
    log.propagate = False
    handle = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    handle.setFormatter(formatter)
    log.addHandler(handle)
    return log


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Connects to a database """
    loggin = mysql.connector.connect(
        host=os.getenv('PERSONAL_DATA_DB_HOST'),
        database=os.getenv('PERSONAL_DATA_DB_NAME'),
        user=os.getenv('PERSONAL_DATA_DB_USERNAME'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD')
    )
    return loggin


def main():
    """read and filter data"""
    db = get_db()
    loggin = get_logger()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    fields = cursor.column_names
    for selected in cursor:
        message = "".join("{}={}; ".format(key, value)
                          for key, value in zip(fields, selected))
        loggin.info(message.strip())
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
