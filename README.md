
# SMMRY API Wrapper for Python

## Getting Started

To get started you'll need to sign up for the app and [register for a partner account](http://smmry.com/partner). In "free mode", you can submit up to 100 requests in 24 hours. Once you obtain your API key, export it as an environment variable in the your shell. (Aternatively, assign your key to a new variable once you're in python.)

**In shell:**


```python
$ export SMMRY_API_KEY='YOUR KEY GOES HERE'
```

**In Python:**


```python
import os

SMMRY_API_KEY = os.environ.get('SMMRY_API_KEY')
```

**Altnernatively...**


```python
SMMRY_API_KEY = 'YOUR KEY GOES HERE'
```

Once your have your key, import the module and create an instance of the Smmry object.


```python
from smmry_api_wrapper import Smmry

smmry = Smmry(SMMRY_API_KEY)
```

## Requesting Summaries

To request the summary for an article pass an article's URL to the `.summarize()` method. A url is the only required parameter, and by default, the method will return a seven-sentence summary. Access the article summary with the `smmry` attribute using dot notation. I'll use this [*Huffington Post* article](https://www.huffingtonpost.com/entry/59ea1e4be4b0542ce4290d0d?section=us_politics) as an example.


```python
url = 'https://www.huffingtonpost.com/entry/59ea1e4be4b0542ce4290d0d?section=us_politics'

huffpost = smmry.summarize(url)

huffpost.smmry
```

**Alternatively, you can customize your requests by adding in optional parameters:**

* **`length`**: Default 7. Must be an int.
* **`with_break`**: Exclude/include page breaks. Default False.
* **`quote`**: Exclude/include quotes. Default False.

**You can view the [full documentation](http://smmry.com/api) on the SMMRY site.**


```python
huffpost = smmry.summarize(url,length=2,with_break=True,quote_avoid=True)

huffpost.smmry
```

Once an article has been succsefull summarized, its summary (`.smmry`), title, character count, sentence length, and URL will be available as object attributes. Additionally, you can select the `.limitation` attribute to view how many requests you have left for that day.


```python
huffpost.title # Accesses article's title
```


```python
huffpost.count # Count of characters
```


```python
huffpost.length # Sentence length
```


```python
huffpost.limitation # API limits
```

**If you prefer, you can use the oject as a python dictionary.**


```python
my_dict = huffpost.smmry_dict

my_dict.keys()
```
