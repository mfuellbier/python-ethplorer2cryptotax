#! /usr/bin/env python
"""
Converts csv export file form Ethplorer to a format, which can be uploaded to cryptotax.
"""
import argparse
import classes.cryptotax as cryptotax
import classes.ethplorer as ethplorer


def find_address(file_name):
    # searches for own ETH address in ethplorer export file
    with open(file_name) as f:
        content = f.readlines()
        addresses = set()
        FIRST_LINE = True
        SECOND_LINE = True
        for line in content:
            line_list = line.strip().split(";")
            if FIRST_LINE:
                FIRST_LINE = False
                continue
            if SECOND_LINE:
                addresses.update([line_list[2], line_list[3]])
                SECOND_LINE = False
                continue
            addresses = addresses.intersection([line_list[2], line_list[3]])
    if len(addresses) == 1:
        return next(iter(addresses))
    else:
        raise NameError("No unique address found.")


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
        "exchange_name", nargs="?", default="Metamask",
        metavar="EXCHANGE NAME", type=str,
        help="Exchange name (Metamask, MyETH, Trezor, Ledger, ...)")

    parser.add_argument(
        "account_name", nargs="?", default="Metamask account 1",
        metavar="ACCOUNT NAME", type=str,
        help="Account name (Metamask Account 1, My ETH Account 2, ...)")

    parser.add_argument(
        "--address", nargs="?", default="",
        metavar="own ETH Address", type=str,
        help="own ETH Address (it will be fetched from input file if ommited)")

    args = parser.parse_args()

    # Find addresss
    if not args.address:
        try:
            own_address = find_address(args.input.name)
        except NameError:
            print("No unique address found. Use --address.")
            return 1
    else:
        own_address = args.address

    # initialize cryptotax_file
    cryptotax_file = cryptotax.cryptotax_file(args.exchange_name, args.account_name)

    # parse ethplorer file and convert to cryptotax file
    with open(str(args.input.name)) as f:
        content = f.readlines()
        FIRST_LINE = True
        for line in content:
            if FIRST_LINE:
                FIRST_LINE = False
                continue
            line_list = line.strip().split(";")
            line_list.append(own_address)
            line_ethplorer = ethplorer.ethplorer_line(*line_list)
            if line_ethplorer.transaction_type == "deposit":
                cryptotaxline = cryptotax.cryptotax_line(line_ethplorer.convert_date(),
                                                         line_ethplorer.symbol,
                                                         "",
                                                         line_ethplorer.value,
                                                         "",
                                                         line_ethplorer.txhash,
                                                         "",
                                                         "",
                                                         line_ethplorer.transaction_type,
                                                         "")
            else:
                cryptotaxline = cryptotax.cryptotax_line(line_ethplorer.convert_date(),
                                                         "",
                                                         line_ethplorer.symbol,
                                                         "",
                                                         line_ethplorer.value,
                                                         line_ethplorer.txhash,
                                                         "",
                                                         "",
                                                         line_ethplorer.transaction_type,
                                                         "")
            cryptotax_file.list.append(cryptotaxline)

    # print cryptotax file to output
    cryptotax_file.print_lines(args.output)


if __name__ == "__main__":
    main()
