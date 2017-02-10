#!/usr/bin/env python3
# Scrape a single Survey Monkey survey that you own with a free account.
# This script alleviates the need to sign up for Survey Monkey's premium plans
# if you just want to export the survey responses in a tabular format
#
# This requires that:
# you own the account: You have full access to the account
# the account is free: I did not test this with an upgraded account
# you wish to scrape just one survey: Designed with only this in mind
#
# cacampbell 2/9/17
from lxml import etree
import requests
import logging



class MonkeyScraperException(Exception):
    def __init__(self, message, errors):
        super(MonkeyScraperException, self).__init__(message)
        self.errors = errors


class MonkeyScraper:
    username = ''
    password = ''
    _monkey = 'https://www.surveymonkey.com'
    _home_url = _monkey + '/home/'
    _login_url = _monkey + '/user/sign-in/'
    _logout_url = _monkey + '/user/sign-out/'
    _logout_button_selector = '//*[@id="dd-my-account"]/ul/li[5]/a'
    _responses_selector = "//*[contains(@class, 'ta-response-item')]"
    _headers = {
            'User-Agent': 'Mozilla/5.0',
            'Upgrade-Insecure-Requests': '1',
            'Host': 'www.surveymonkey.com',
            'Origin': _monkey,
            'Referer': _monkey
        }
    _session = requests.session()

    def __init__(self, *args, **kwargs):
        if args:
            self.username = args[0]
            self.password = args[1]
        if kwargs:
            if 'username' in kwargs.keys():
                self.username = kwargs['username']
            if 'password' in kwargs.keys():
                self.password = kwargs['password']

    def __enter__(self):
        self.init()
        self.log_in()
        return self

    def __exit__(self, ex_type, ex_val, traceback):
        if traceback:
            logging.log(level=logging.CRITICAL, msg=traceback)

        self.log_out()
        self.close()

    def _get_cookies(self):
        # These are apparently the cookies that are necessary for navigating
        # the SurveyMonkey site without running into forbidden errors (403)
        _cookie_keys = keys = ['SSLB', 'apex__sm', 'auth', 'session', 'sm_rec',
                               'ep201', 'ep202', 'tld_user', 'tld_set',
                               'endpages_seen', 'SSRT', 'ucs_topbar_views']
        if self._session.cookies:
            cookies = {}
            for key in _cookie_keys:
                try:
                    cookies[key] = self._session.cookies[key]
                except KeyError:
                    pass
            return cookies
        else:
            raise(
                MonkeyScraperException(
                    "Premature Cookie Robbery",
                    {"No Cookies": "The session CookieJar is empty"}
                )
            )

    def _get(self, url='', headers=None, **kwargs):
        # Wrap get to allow keyword usage
        return(self._session.get(url=url, headers=headers, data=kwargs))

    def _post(self, url='', headers=None, **kwargs):
        # Wrap post to allow keyword usage
        return(self._session.post(url=url, headers=headers, data=kwargs))

    def _check_code(self, resp):
        c = resp.status_code

        if c != 200:
            raise(
                MonkeyScraperException(
                    "Not Okay (200)",
                    {
                        '{}'.format(c),
                        'Server sent {}. Expected 200.'.format(c)
                    }
                )
            )

    def _page_root(self, response):
        return etree.HTML(response.content)

    def _logged_in(self):
        # Check if logged in by looking for a log-out button on the home
        # page.
        resp = self._get(url=self._home_url,
                         headers=self._headers,
                         **self._get_cookies())
        self._check_code(resp)
        LOGOUT_BUTTON = etree.XPath(self._logout_button_selector)
        try:
            LOGOUT_BUTTON(self._page_root(resp))[0]  # exists?
        except IndexError as err:
            return False

        return True


    def check_logged_in(self):
        # If not logged in, scream about it
        if not self._logged_in():
            raise(
                MonkeyScraperException(
                    "Logged Out",
                    {
                        "Logged Out",
                        "The session was unexpectedly logged out"
                    }
                )
            )

    def init(self):
        # Need to have the server send back cookies needed for navigating
        # the site. I chose the log in url because this is needed anyway and
        # harmlessly redirects to the home page if already logged in.
        self._get(url=self._login_url, headers=self._headers)

    def log_in(self, username='', password=''):
        if self._logged_in():
            logging.log(level=logging.WARNING, msg='Already logged in')
            return

        if not username:
            username = self.username
        if not password:
            password = self.password
        if not (username and password):
            raise(
                MonkeyScraperException(
                    "LogIn Failed",
                    {'Incorrect Arguments': 'Required: username and password'}
                )
            )

        login_headers = dict(self._headers)
        login_headers['Referer'] = self._login_url

        resp = self._post(
            url=self._login_url,
            headers=login_headers,
            username=username,
            password=password,
            **self._get_cookies()
        )

        self._check_code(resp)
        self.check_logged_in()

    def _get_analyze_page_root(self, survey_url):
        self.check_logged_in()
        headers = dict(self._headers)
        headers['Referer'] = survey_url
        survey_page = self._get(survey_url,
                                headers=headers,
                                **self._get_cookies())
        self._check_code(survey_page)
        return self._page_root(survey_page)

    def scrape(self, survey_url):
        page = self._get_analyze_page_root(survey_url)
        print(page)

    def create_db(self, survey_url):
        page = self._get_analyze_page_root(survey_url)
        print(page)

    def log_out(self):
        logout_headers = dict(self._headers)
        logout_headers['Referer'] = self._home_url
        if self._logged_in():
            resp = self._get(
                url=self._logout_url,
                headers=logout_headers,
                **self._get_cookies()
            )
            self._check_code(resp)
        else:
            logging.log(level=logging.WARNING, msg='Already logged out')

    def close(self):
        self._session.close()