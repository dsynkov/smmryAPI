import pandas as pd
import argparse
import pathlib
import csv
import os

from smmryapi import SmmryAPIException
from smmryapi import SmmryAPI


def get_arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument('key', help="Input your SMMRY API key.")

    parser.add_argument('path', help="Path to you file containing URLs.")

    parser.add_argument('-l', '--length', type=int, default=7,
                        help="Select the sentence length for the summaries.")

    parser.add_argument('-k', '--keywords', type=int, default=3,
                        help="Select the number of keywords to return.")

    return parser.parse_args()


def parse_input_file(path):

    abspath = os.path.abspath(path)

    name, ext = os.path.splitext(abspath)

    if ext == '.xlsx' or ext == '.xls':
        df = pd.read_excel(
            abspath,
            cols='A',
            header=None
        )

        urls = df.iloc[:, 0].tolist()

    elif ext == '.txt' or ext == '.cxv':
        urls = open(abspath, 'r').read().splitlines()

    else:
        raise SmmryAPIException("URLs must be in a single-column \
            .txt, .csv, .xlsx, or .xls file.")

    return urls, name


def get_output_filename(name):

    path = pathlib.PurePath(os.getcwd())

    return str(path/'exports'/(name+'-summaries.csv'))


def main():

    args = get_arguments()
    urls, name = parse_input_file(args.path)
    output_file = get_output_filename(name)

    print(output_file)

    with open(output_file, 'w', newline="", encoding='utf-8') as file:
        writer = csv.writer(file, dialect='excel')
        writer.writerow([
            'url',
            'summary',
            'length',
            'title',
            'reduction',
            'keyword_count',
            'keyword_array'
        ])

        smmry = SmmryAPI(args.key)

        total_urls = len(urls)

        successful_urls = 0

        for url in urls:

            try:
                s = smmry.summarize(
                    url,
                    sm_length=args.length,
                    sm_keyword_count=args.keywords
                )

                successful_urls += 1

                writer.writerow([
                    url,
                    s.sm_api_content,
                    s.length,
                    s.sm_api_title,
                    s.sm_api_content_reduced,
                    args.keywords,
                    s.sm_api_keyword_array
                ])

            except SmmryAPIException as e:
                print(e, url)

        print("\nSuccess! A total of %s out of %s summaries have been retrieved.\n"
              % (successful_urls, total_urls))

        print("You have %s requests remaining for today.\n"
              % s.requests_remaining)


if __name__ == '__main__':
    main()
