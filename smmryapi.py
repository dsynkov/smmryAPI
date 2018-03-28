import requests
import tldextract


class SmmryAPIException(Exception):
    pass


class SmmryAPI:

    def __init__(self, key):
        self.key = key
        self.endpoint = 'http://api.smmry.com/'

    def summarize(self, url, **kwargs):
        params = {k.upper(): v for k, v in kwargs.items()}

        params['SM_URL'] = url
        params['SM_API_KEY'] = self.key

        response = requests.get(self.endpoint, params=params)
        response.close()

        smmry_dict = response.json()

        if smmry_dict.get('sm_api_error'):
            raise SmmryAPIException("%s: %s" % (smmry_dict['sm_api_error'], smmry_dict['sm_api_message']))

        smmry_dict['sm_api_content'] = smmry_dict['sm_api_content'].strip()

        return Summary(smmry_dict, params, response)


class Summary:

    def __init__(self, smmry_dict, params, response):

        self.smmry_dict = smmry_dict
        self.url = response.url
        self.params = params
        self.domain = self.get_domain_name(params)

        for key, value in smmry_dict.items():
            setattr(self, key, value)

        self.length = 7  # Default

        if params.get('SM_LENGTH'):
            self.length = params['SM_LENGTH']

    def get_domain_name(self, params):

        extract = tldextract.extract(params['SM_URL'])

        return '.'.join([extract.domain, extract.suffix])

    def __str__(self):
        return self.sm_api_content

    def __len__(self):
        return self.length

    def __iter__(self):
        for key, value in self.smmry_dict.items():
            yield (key, value)
