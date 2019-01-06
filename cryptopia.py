#! /usr/bin/env python
"""
Converts csv export file from Cryptopia to a format, which can be uploaded to cryptotax.
"""
import argparse
import classes.cryptotax as cryptotax
import classes.cryptopia as cryptopia
import re


def main():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        "input", default="-",
        metavar="INPUT_FILE", type=argparse.FileType("r"),
        help="path to the input file")

    parser.add_argument(
        "--output", nargs="?", default=None,
        metavar="OUTPUT_FILE", type=argparse.FileType("w"),
        help="path to the output file (write to stdout if omitted)")

    parser.add_argument(
        "account_name", nargs="?", default="Cryptopia_1",
        metavar="ACCOUNT NAME", type=str,
        help="Account name (Metamask Account 1, My ETH Account 2, ...)")

    args = parser.parse_args()

    # initialize cryptotax_file
    exchange_name = "Cryptopia"
    cryptotax_file = cryptotax.cryptotax_file(exchange_name, args.account_name)

    TRANSACTION_TYPE = ""

    # parse cryptopia file and convert to cryptotax file
    with args.input as f:
        content = f.readlines()
        FIRST_LINE = True
        for line in content:
            line = re.sub(r'"[^"]*$', '', line[1::])
            if FIRST_LINE:
                if "Fee" in line:
                    # Withdraw_History
                    TRANSACTION_TYPE = "withdrawal"
                else:
                    # Deposit_History
                    TRANSACTION_TYPE = "deposit"
                FIRST_LINE = False
                continue
            line_list = line.strip().split('","')
            if TRANSACTION_TYPE == "deposit":
                line_cryptopia = cryptopia.cryptopia_line(line_list[1], line_list[2], line_list[5], None, None, None, line_list[7], TRANSACTION_TYPE)
            elif TRANSACTION_TYPE == "withdrawal":
                line_cryptopia = cryptopia.cryptopia_line(line_list[1], line_list[2], None, line_list[3], line_list[5], line_list[6], line_list[7], TRANSACTION_TYPE)
            else:
                print("Error, no TRANSACTION_TYPE")
                return 1

            # Convert cryptopia_line to cryptotax_line
            if line_cryptopia.transaction_type == "deposit":
                cryptotaxline = cryptotax.cryptotax_line(line_cryptopia.convert_date(),
                                                         line_cryptopia.currency,
                                                         "",
                                                         line_cryptopia.amount,
                                                         "",
                                                         line_cryptopia.transaction,
                                                         "",
                                                         "",
                                                         line_cryptopia.transaction_type,
                                                         "")
            else:
                cryptotaxline = cryptotax.cryptotax_line(line_cryptopia.convert_date(),
                                                         "",
                                                         line_cryptopia.currency,
                                                         "",
                                                         line_cryptopia.amount,
                                                         line_cryptopia.transactionid,
                                                         line_cryptopia.fee,
                                                         line_cryptopia.currency,
                                                         line_cryptopia.transaction_type,
                                                         "")
            cryptotax_file.list.append(cryptotaxline)

    # print cryptotax file to output
    cryptotax_file.print_lines(args.output)


if __name__ == "__main__":
    main()
