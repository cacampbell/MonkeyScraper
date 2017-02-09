# MonkeyScraper
HTML Scraper for SurveyMonkey Free Accounts

What's that? Survey Monkey has an API you can use? Oh. Cool. ... 

Basically, I was very annoyed with the inability to export survey results if your account is free at survey monkey.
Rather than tacitly accepting this annoyance (and manually gathering every survey response), I wrote this
HTML scraper to do this for me.

See MonkeyScraper.py for the implementation of this class, and see monkey_scraper.py for an example usage.
Unlike with Sympa, where the horrible web interface made me want to write a scraper just so that I didn't kill
myself, this is meant only for the task of finding the responses of single surveys. 

However, this could likewise be explanded to be a full management tool. In any case, please fork me bby.

### Example

```python
from MonkeyScraper import MonkeyScraper
from sys import argv


def main(username, password):
    scraper = MonkeyScraper()
    scraper.init()
    scraper.log_in(username=username, password=password)
    print(scraper)  # Or do other stuff
    # ...
    scraper.scrape('<survey summary page url>', format='csv', file='<output file or blank for stdout>')
    # ...
    scraper.log_out()
    scraper.close()
    
    #  Can also use context management to do this
    #  with MonkeyScraper(username=username, password=password) as scraper:
        #  print(scraper)  # Or do other stuff
        # ...
        #  scraper.scrape('<survey summary page url>', format='csv', file='<output file or blank for stdout>')
        

if __name__ == '__main__':
    main(*argv[1:])
```
