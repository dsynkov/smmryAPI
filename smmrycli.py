import pandas as pd
import argparse
import pathlib
import csv
import os

from urllib.parse import urlparse
from smmryapi import SmmryAPI
from smmryapi import SmmryAPIException


def get_arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument('key', help="Input your SMMRY API key.")

    parser.add_argument('path', help="Path to you file containing URLs.")

    parser.add_argument('-l', '--length', type=int, default=7,
                        help="Select the sentence length for the summaries.")

    parser.add_argument('-k', '--keywords', type=int, default=3,
                        help="Select the number of keywords to return.")

    parser.add_argument('-b', '--with_break', action='store_true',
                        help="Select to include [BREAK] (default False).")

    parser.add_argument('-r', '--replace_break', type=str,
                        help="If -b is selected, select what you want to replace [BREAK] with.")

    parser.add_argument('-q', '--quote_avoid', action='store_true',
                        help="Select if you want to avoid quotes in your summary.")

    return parser.parse_args()


def parse_input_file(path):

    abspath = os.path.abspath(path)

    _, ext = os.path.splitext(abspath)
    name = os.path.basename(path).split('.')[0]

    if ext == '.xlsx' or ext == '.xls':
        df = pd.read_excel(
            abspath,
            cols='A',
            header=None
        )

        urls = df.iloc[:, 0].tolist()

    elif ext == '.txt' or ext == '.csv':
        urls = open(abspath, 'r').read().splitlines()

    else:
        raise Exception("URLs must be in a single-column .txt, .csv, .xlsx, or .xls file.")

    if len(urls) == 0:
        raise Exception("File %s does not contain any URLs." % path)

    return urls, name


def get_output_filename(name):

    path = pathlib.PurePath(os.getcwd())

    export_path = path / 'exports' / (name + '-summaries.csv')

    return str(export_path)


def validate_url(urls):

    good_urls = []

    for url in urls:
        result = urlparse(url)

        if len(result.netloc) == 0:
            print("Invalid url: %s" % url)
        else:
            good_urls.append(url)

    if len(good_urls) == 0:
        raise Exception("File does not contain any working URLs.")

    return good_urls


def main():

    args = get_arguments()

    urls, name = parse_input_file(args.path)
    output_file = get_output_filename(name)

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

        requests_remaining = ''
        total_urls = len(urls)
        successful_urls = 0

        good_urls = validate_url(urls)

        for url in good_urls:

            try:
                s = smmry.summarize(
                    url,
                    sm_length=args.length,
                    sm_keyword_count=args.keywords,
                    sm_with_break=args.with_break,
                    sm_break_with=args.replace_break
                )

                successful_urls += 1

                writer.writerow([
                    url,
                    s.sm_api_content,
                    s.sm_length,
                    s.sm_api_title,
                    s.sm_api_content_reduced,
                    args.keywords,
                    s.sm_api_keyword_array
                ])

                requests_remaining = s.sm_requests_remaining

            except SmmryAPIException as e:
                print(e, url)

        print("\nSuccess! A total of %s out of %s summaries have been retrieved.\n"
              % (successful_urls, total_urls))

        print("You have %s requests remaining for today."
              % requests_remaining)


if __name__ == '__main__':
    main()
