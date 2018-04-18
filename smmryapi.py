import requests
import collections
from summary import Summary


class SmmryAPIException(Exception):
    pass


class SmmryAPI:

    def __init__(self, key):

        self.key = key
        self.max = 40  # Max number of sentences
        self.endpoint = 'http://api.smmry.com/'

        self.bool_params = [
            'sm_with_break',
            'sm_with_encode',
            'sm_ignore_length',
            'sm_quote_avoid',
            'sm_question_avoid',
            'sm_exclamation_avoid'
        ]

    def check_length(self, kwargs_dict):

        if kwargs_dict.get('sm_length'):
            if kwargs_dict['sm_length'] > self.max:
                kwargs_dict['sm_length'] = self.max

        return kwargs_dict

    def check_bool(self, kwargs_dict):

        keys_to_drop = []

        for key, value in kwargs_dict.items():
            if key in self.bool_params and not value:
                    keys_to_drop.append(key)

        for key in keys_to_drop:
            kwargs_dict.pop(key)

        return kwargs_dict

    def kwargs2params(self, url, kwargs_dict):

        params_length = self.check_length(kwargs_dict)
        params_bool = self.check_bool(params_length)

        params = collections.OrderedDict(params_bool)

        # Note: The parameter &SM_URL= should always be at the end of the
        # request url to avoid complications (see https://smmry.com/api).
        params.update({'sm_api_key': self.key})
        params.update({'sm_url': url})
        params.move_to_end('sm_url')

        return {k.upper(): v for k, v in params.items()}

    def summarize(self, url, **kwargs):

        params = self.kwargs2params(url, kwargs)

        response = requests.get(self.endpoint, params=params)
        response.close()

        smmry_dict = response.json()

        if smmry_dict.get('sm_api_error'):
            raise SmmryAPIException("%s: %s" % (smmry_dict['sm_api_error'], smmry_dict['sm_api_message']))

        if params.get('SM_WITH_BREAK'):
            smmry_dict['sm_api_content'] = smmry_dict['sm_api_content'].replace('[BREAK]', params['SM_BREAK_WITH'])

        smmry_dict['sm_api_content'] = smmry_dict['sm_api_content'].strip()

        return Summary(smmry_dict, params, response)
