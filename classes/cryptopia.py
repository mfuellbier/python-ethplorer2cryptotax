#! /usr/bin/env python

import datetime


class cryptopia_line:

    WITHDRAW = "withdrawal"
    DEPOSIT = "deposit"

    def __init__(self, currency, amount, transaction, fee, transactionid, address, timestamp, transaction_type):
        self.timestamp = timestamp
        self.transaction = transaction
        if not fee:
            fee = 0
        self.amount = str(float(amount)-float(fee))
        self.currency = currency
        self.fee = fee
        self.transactionid = transactionid
        self.address = address
        self.transaction_type = transaction_type

    def convert_date(self):
        return datetime.datetime.strptime(self.timestamp, "%d/%m/%Y %I:%M:%S %p").strftime("%d.%m.%Y %H:%M:%S")
