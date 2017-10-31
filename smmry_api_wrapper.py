import json
import requests

SMMRY_API_URL = 'http://api.smmry.com/'

smmry_param_dict = {
    'length': 'SM_LENGTH=',
    'count': 'SM_KEYWORD_COUNT=',
    'quote_avoid': 'SM_QUOTE_AVOID',
    'with_break': 'SM_WITH_BREAK'
}

smmry_response_dict = {
    'sm_api_message': 'message',
    'sm_api_character_count': 'count',
    'sm_api_title': 'title',
    'sm_api_content': 'smmry',
    'sm_api_keyword_array': 'keywords',
    'sm_api_error': 'error',
    'sm_api_limitation': 'limitation'
}

smmry_str_error_msg = """

You must call Smmry.summarize() with at least a url 
before converting the Smmry object into a string.

"""
smmry_len_error_msg = """

You must call Smmry.summarize() with at least a url 
before accessing a Smmry object's length.

"""

class Smmry:
    
    def __init__(self,key):
        self.key = key
    
    def __str__(self):
        try:
            return self.smmry
        except (AttributeError, TypeError):
            print(smmry_str_error_msg)
            
    def __len__(self):
        try:
            return self.length
        except (AttributeError, TypeError):
            print(smmry_len_error_msg)
    
    def summarize(self, url, **kwargs):
        
        required_parameter_key = 'SM_API_KEY='
        required_parameter_url = 'SM_URL='
        
        sep = '&'
        
        # Create three replacement fields
        # to populate the url path 
        fields = '{}' * 3
        
        # Build required url path
        path = SMMRY_API_URL + fields.format(
            sep, required_parameter_key, self.key)

        if kwargs:
            for key,value in kwargs.items():
                # Build optional url path
                if not isinstance(value,bool):
                    # For int parameters append both key and value
                    optional_parameter = sep + smmry_param_dict[key] + str(value)
                    path += optional_parameter
                elif value:
                    # For bool parameters set to True append only key
                    optional_parameter = sep + smmry_param_dict[key]
                    path += optional_parameter
        
        # Var &SM_URL must be at end of call
        path += sep + required_parameter_url + url
        
        r = requests.get(path)
        
        # Create json dict
        r_dict = r.json()
        
        # Handle error codes
        if 'sm_api_error' in r_dict.keys():
            raise Exception('SM_API_ERROR {}: {}.'.format(
                r_dict['sm_api_error'],
                r_dict['sm_api_message']))
        
        # Strip white space from contents
        r_dict['sm_api_content'] = r_dict['sm_api_content'].strip()
        
        # Create empty dict
        self.smmry_dict = {}
        
        for key,value in r_dict.items():
            # Get new dict key names 
            new_key = smmry_response_dict[key]
            # Populate empty new dict
            self.smmry_dict[new_key] = value
            # Set dict contents as attributes
            setattr(self,new_key,value)
        
        # Make some edits to attrs
        self.count = int(self.count)
        
        # Add additional attrs from parameters
        if 'length' in kwargs.keys():
            self.length = kwargs['length']
        else:
            # Set default length
            self.length = 7
        self.url = url
                
        return self