from sys import argv
from MonkeyScraper import MonkeyScraper


def main(username, password, survey_url):
    """
    Creates a MonkeyScraper, logs in, and scrapes the survey at the provided url
    :param username: str: surveymonkey username
    :param password: str: surveymonkey password
    :param survey_url: str: the "summary" page url for your survey
    :return:
    """
    scraper = MonkeyScraper()
    scraper.init()
    scraper.log_in(username=username, password=password)
    print(scraper)
    scraper.log_out()
    scraper.close()

    with MonkeyScraper(username=username, password=password) as scraper:
        print(scraper)


if __name__ == '__main__':
    main(*argv[1:])