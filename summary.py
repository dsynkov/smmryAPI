import re
import tldextract


class Summary:

    def __init__(self, smmry_dict, params, response):

        self.params = params
        self.api_url = response.url
        self.sm_url = params['SM_URL']
        self.smmry_dict = smmry_dict

        self.sm_domain = self.get_domain_name(params)
        self.sm_requests_remaining = self.requests_remaining(smmry_dict)

        for key, value in smmry_dict.items():
            setattr(self, key, value)

        self.sm_length = 7  # Default
        if params.get('SM_LENGTH'):
            self.sm_length = params['SM_LENGTH']

        self.smmry_dict['sm_domain'] = self.sm_domain
        self.smmry_dict['sm_length'] = self.sm_length
        self.smmry_dict['sm_requests_remaining'] = self.sm_requests_remaining

    def __str__(self):
        return self.sm_api_content

    def __len__(self):
        return self.sm_length

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
