#! /usr/bin/env python


class cryptotax_file:

    HEADLINE = "exchange_name,account_name,trade_date,buy_asset,sell_asset,buy_amount,sell_amount,exchange_order_id,fee,fee_asset,transaction_type,clarification"

    def __init__(self, exchange_name, account_name):
        self.exchange_name = exchange_name
        self.account_name = account_name
        self.list = []  # list of cryptotax_lines

    def print_lines(self, output_file=None):
        if output_file:
            output_file.write(self.HEADLINE)
            output_file.write("\r\n")
        else:
            print(self.HEADLINE)

        for line in self.list:
            try:
                if output_file:
                    output_file.write(line.print_line(self.exchange_name, self.account_name))
                    output_file.write("\r\n")
                else:
                    print(line.print_line(self.exchange_name, self.account_name))
            except TypeError:
                #TODO
                raise TypeError


class cryptotax_line():

    def __init__(self, trade_date, buy_asset, sell_asset, buy_amount, sell_amount, exchange_order_id, fee, fee_asset, transaction_type, deposit_clarification):
        self.trade_date = trade_date
        self.buy_asset = buy_asset
        self.sell_asset = sell_asset
        self.buy_amount = buy_amount
        self.sell_amount = sell_amount
        self.exchange_order_id = exchange_order_id
        self.fee = fee
        self.fee_asset = fee_asset
        self.transaction_type = transaction_type
        self.deposit_clarification = deposit_clarification

    def print_line(self, exchange_name, account_name):
        # Prints the line for the cryptotax import file
        result = (exchange_name + "," +
                  account_name + "," +
                  self.trade_date + "," +
                  self.buy_asset + "," +
                  self.sell_asset + "," +
                  self.buy_amount + "," +
                  self.sell_amount + "," +
                  self.exchange_order_id + "," +
                  self.fee + "," +
                  self.fee_asset + "," +
                  self.transaction_type + "," +
                  self.deposit_clarification)
        if result[-1] == ",":
            return result[0:-1]
        else:
            return result
