import requests
import tldextract
import collections
import re


class SmmryAPIException(Exception):
    pass


class SmmryAPI:

    def __init__(self, key):
        self.key = key
        self.max = 40  # Max number of sentences
        self.endpoint = 'http://api.smmry.com/'

    def summarize(self, url, **kwargs):

        kwargs = {k.upper(): v for k, v in kwargs.items()}

        # "Note: The parameter &SM_URL= should always be at the end of the
        # request url to avoid complications" (see https://smmry.com/api).
        params = collections.OrderedDict(kwargs)
        params.update({'SM_API_KEY': self.key})
        params.update({'SM_URL': url})
        params.move_to_end('SM_URL')

        if params.get('SM_LENGTH'):
            if params['SM_LENGTH'] > 40:
                params['SM_LENGTH'] = 40

        response = requests.get(self.endpoint, params=params)
        response.close()

        smmry_dict = response.json()

        if smmry_dict.get('sm_api_error'):
            raise SmmryAPIException("%s: %s" % (smmry_dict['sm_api_error'], smmry_dict['sm_api_message']))

        smmry_dict['sm_api_content'] = smmry_dict['sm_api_content'].strip()

        return Summary(smmry_dict, params, response)


class Summary:

    def __init__(self, smmry_dict, params, response):

        self.domain = self.get_domain_name(params)
        self.params = params
        self.url = response.url
        self.smmry_dict = smmry_dict
        self.requests_remaining = self.requests_remaining(smmry_dict)

        for key, value in smmry_dict.items():
            setattr(self, key, value)

        self.length = 7  # Default
        if params.get('SM_LENGTH'):
            self.length = params['SM_LENGTH']

    def __str__(self):
        return self.sm_api_content

    def __len__(self):
        return self.length

    def __iter__(self):
        for key, value in self.smmry_dict.items():
            yield (key, value)

    def get_domain_name(self, params):

        extract = tldextract.extract(params['SM_URL'])

        return '.'.join([extract.domain, extract.suffix])

    def requests_remaining(self, smmry_dict):

        pattern = r'\d+'
        message = smmry_dict['sm_api_limitation'].split(',')[1]
        match = re.search(pattern, message)

        return int(match.group())

