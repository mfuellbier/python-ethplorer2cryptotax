#! /usr/bin/env python

import datetime


class ethplorer_line:

    WITHDRAW = "withdraw"
    DEPOSIT = "deposit"

    def __init__(self, date, txhash, from_address, to_address, token_name, token_address, value, usdPrice, symbol, own_address):
        self.date = date
        self.txhash = txhash
        self.from_address = from_address
        self.to_address = to_address
        self.token_name = token_name
        self.token_address = token_address
        self.value = value.replace(",", ".")
        self.usdPrice = usdPrice
        self.symbol = symbol
        self.own_address = own_address

        if self.from_address == own_address:
            self.transaction_type = self.WITHDRAW
        elif self.to_address == own_address:
            self.transaction_type = self.DEPOSIT
        else:
            self.transaction_type = ""

    def convert_date(self):
        return datetime.datetime.strptime(self.date, "%Y-%m-%d %H:%M:%S").strftime("%d.%m.%Y %H:%M:%S")
