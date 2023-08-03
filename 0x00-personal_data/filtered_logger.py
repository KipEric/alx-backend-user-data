#!/usr/bin/env python3
"""
F unction to obfuscate log message fields using reqular expression
"""


import logging
import re
from typing import List
import os
import mysql.connector


PII_FIELDS = [
        'name',
        'email',
        'ssn',
        'password',
        'ip',
        'last_login',
        'user_agent'
        ]


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str
        ) -> str:
    """
    Function that obfuscates the specific fields in the log message
    """
    for field in fields:
        message = re.sub(f"{field}=[^;]*", f"{field}={redaction}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Function that obfuscates the specific fields in the log message
        """
        record.msg = filter_datum(self.fields, self.REDACTION, record.msg, ';')
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """
    Creates and returns a loging.Logger object
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger


def get_db():
    """
    Return a connection to the database
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=db_name
    )


def main():
    """
    Main function to obtain a database connection
    """
    PII_FIELDS = [
        'name',
        'email',
        'ssn',
        'password',
        'ip',
        'last_login',
        'user_agent'
        ]

    logger = get_logger()

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    for row in cursor:
        msg = f"name={row[0]};
        email={row[1]};
        ssn={row[2]};
        password={row[3]};
        ip={row[4]};
        last_login={row[5]};
        user_agent={row[6]}"
        logger.info(msg)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
