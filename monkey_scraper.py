from sys import argv
import logging
from MonkeyScraper import MonkeyScraper

LOG_FILENAME = 'MonkeyScraper.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)


def main(username, password, survey_url):
    """
    Creates a MonkeyScraper, logs in, and scrapes the survey at the provided url
    :param username: str: surveymonkey username
    :param password: str: surveymonkey password
    :param survey_url: str: the "analyze" page url for your survey
    :return:
    """
    # scraper = MonkeyScraper()
    # scraper.init()
    # scraper.log_in(username=username, password=password)
    # scraper.scrape(survey_url)
    # scraper.log_out()
    # scraper.close()

    with MonkeyScraper(username=username, password=password) as scraper:
        survey = scraper.scrape(survey_url)


if __name__ == '__main__':
    main(*argv[1:])