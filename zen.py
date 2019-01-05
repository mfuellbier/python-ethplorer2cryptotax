#! /usr/bin/env python
"""
Converts csv export file form Ethplorer to a format, which can be uploaded to cryptotax.
"""
import argparse
import classes.cryptotax as cryptotax
import classes.zen as zen
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
        "account_name", nargs="?", default="Zen_1",
        metavar="ACCOUNT NAME", type=str,
        help="Account name (Metamask Account 1, My ETH Account 2, ...)")

    parser.add_argument(
        "--address", nargs="?", default="",
        metavar="own ETH Address", type=str,
        help="own ETH Address (it will be fetched from input file if ommited)")

    args = parser.parse_args()

    # initialize cryptotax_file
    exchange_name = "generic"
    cryptotax_file = cryptotax.cryptotax_file(exchange_name, args.account_name)

    # parse zen file and convert to cryptotax file
    with args.input as f:
        content = f.readlines()
        FIRST_LINE = True
        for line in content:
            line = re.sub(r'"[^"]*$', '', line[1::])
            if FIRST_LINE:
                FIRST_LINE = False
                continue
            line_list = line.strip().split('","')
            if line_list[6] == "0.00000000":
                # No zen mined
                continue
            line_zen = zen.zen_line(*line_list)

            # Convert zen_line to cryptotax_line
            if not line_zen.paid == "-":
                cryptotaxline = cryptotax.cryptotax_line(line_zen.convert_date(),
                                                         "ZEN",
                                                         "",
                                                         line_zen.zen,
                                                         "",
                                                         line_zen.transaction_id,
                                                         "",
                                                         "",
                                                         "deposit",
                                                         "")
                cryptotax_file.list.append(cryptotaxline)
            else:
                # Not paid yet
                print("[+] ID " + line_zen.ID + " not paid yet.")

    # print cryptotax file to output
    cryptotax_file.print_lines(args.output)


if __name__ == "__main__":
    main()
