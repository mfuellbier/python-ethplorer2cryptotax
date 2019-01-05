#! /usr/bin/env python

import datetime


class zen_line:

    def __init__(self, ID, PM, period_start, period_end, status, uptime, zen, created, paid, transaction_id):
        self.ID = ID
        self.PM = PM
        self.period_start = period_start
        self.period_end = period_end
        self.status = status
        self.uptime = uptime
        self.zen = zen
        self.created = created
        self.paid = paid
        self.transaction_id = transaction_id

    def convert_date(self):
        return datetime.datetime.strptime(self.paid, "%Y-%m-%d %H:%M:%S").strftime("%d.%m.%Y %H:%M:%S")
