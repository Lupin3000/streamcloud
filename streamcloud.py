# -*- coding: utf-8 -*-
"""streamcloud.eu download main file"""

import argparse
import logging
import pycurl
import sys
import time

import lxml.etree
import requests
import validators


class Streamcloud(object):
    """streamcloud.eu download main class"""

    @staticmethod
    def __parse_arguments():
        """
        parse given arguments

        @return: class
        """

        description = 'streamcloud.eu download by Python'
        parser = argparse.ArgumentParser(description=description)

        parser.add_argument("-v", "--verbosity",
                            action="count",
                            help="increase output verbosity")
        parser.add_argument("-o", "--output",
                            type=str,
                            default="video.mp4",
                            help="set output file name")
        parser.add_argument("url", help="streamcloud.eu video url")

        return parser.parse_args()

    @staticmethod
    def __progress(to_download, downloaded, to_upload, uploaded):
        """print download progress to stdout"""

        del to_upload
        del uploaded

        if to_download != 0 and downloaded != 0:

            percent_completed = float(downloaded) / to_download
            rate = round(percent_completed * 100, ndigits=2)
            completed = "#" * int(rate)
            spaces = " " * (100 - int(rate))

            sys.stdout.write('\r[%s%s] %s%%' % (completed, spaces, rate))
            sys.stdout.flush()

    def __init__(self):
        """streamcloud.eu download constructor"""

        dash = '-' * 100
        sys.stdout.write('%s\n' % dash)

        log_format = '%(asctime)s %(levelname)s: %(message)s'

        self.__logger = logging.getLogger(__name__)

        args = Streamcloud.__parse_arguments()

        if args.verbosity > 1:
            logging.basicConfig(format=log_format,
                                filename='debug.log',
                                level=logging.DEBUG)
        elif args.verbosity == 1:
            logging.basicConfig(format=log_format,
                                filename='info.log',
                                level=logging.INFO)
        else:
            logging.basicConfig(format=log_format,
                                level=logging.ERROR)

        self.__args = args
        self.__params = dict()
        self.__seconds = 15
        self.__video_url = str()

    def __verify_url(self):
        """
        verify that url is valid

        @return: bool
        """

        self.__logger.info('Verify that %s is valid url', self.__args.url)

        if not validators.url(self.__args.url):
            return False
        else:
            return True

    def __get_post_params(self):
        """parse needed POST params from given URL"""

        self.__logger.info('Parse params from %s', self.__args.url)

        xpath_op = './/input[@name="op"]'
        xpath_usr_login = './/input[@name="usr_login"]'
        xpath_id = './/input[@name="id"]'
        xpath_fname = './/input[@name="fname"]'
        xpath_referer = './/input[@name="referer"]'
        xpath_hash = './/input[@name="hash"]'
        xpath_imhuman = './/input[@name="imhuman"]'

        try:
            req = requests.get(self.__args.url)
            html_source = req.text
        except requests.exceptions.RequestException as error:
            self.__logger.error(error)
            sys.exit(1)

        self.__params['op'] = lxml.etree.HTML(
            html_source).find(xpath_op).attrib['value']
        self.__params['usr_login'] = lxml.etree.HTML(
            html_source).find(xpath_usr_login).attrib['value']
        self.__params['id'] = lxml.etree.HTML(
            html_source).find(xpath_id).attrib['value']
        self.__params['fname'] = lxml.etree.HTML(
            html_source).find(xpath_fname).attrib['value']
        self.__params['referer'] = lxml.etree.HTML(
            html_source).find(xpath_referer).attrib['value']
        self.__params['hash'] = lxml.etree.HTML(
            html_source).find(xpath_hash).attrib['value']
        self.__params['imhuman'] = lxml.etree.HTML(
            html_source).find(xpath_imhuman).attrib['value']

        self.__logger.debug(self.__params)

    def __extract_video_url(self):
        """extract video url from streamcloud.eu"""

        self.__logger.info('wait for %s seconds', self.__seconds)

        time.sleep(self.__seconds)

        self.__logger.info('Extract video url from %s', self.__args.url)

        try:
            req = requests.post(self.__args.url, data=self.__params)
            html_source = req.text
        except requests.exceptions.RequestException as error:
            self.__logger.error(error)
            sys.exit(1)

        self.__logger.debug(html_source)

        xpath_script = './/div[@id="player_code"]/script[3]'
        script = lxml.etree.HTML(html_source).find(xpath_script).text

        self.__logger.debug(script)

        text = script.split(',')
        url = text[2]
        self.__video_url = url[9:-1]

        self.__logger.debug(self.__video_url)

    def __download_file(self):
        """download video from streamcloud.eu"""

        self.__logger.info('start download as %s', self.__args.output)

        video_file = open(self.__args.output, "wb")
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, self.__video_url)
        curl.setopt(pycurl.WRITEDATA, video_file)
        curl.setopt(curl.NOPROGRESS, False)
        curl.setopt(curl.XFERINFOFUNCTION, Streamcloud.__progress)
        curl.perform()
        curl.close()
        video_file.close()

        self.__logger.info('finish download as %s', self.__args.output)

    def verify_arguments(self):
        """verify application arguments"""

        self.__logger.debug(self.__args.url)

        if not self.__verify_url():
            sys.exit(1)

    def download_video(self):
        """running needed methods"""

        sys.stdout.write('> STEP 1: Extract video file information\n')
        self.__get_post_params()

        sys.stdout.write('> STEP 2: Extract video file url\n')
        self.__extract_video_url()

        sys.stdout.write('> STEP 3: Start video file download\n')
        self.__download_file()

if __name__ == "__main__":
    RUN = Streamcloud()
    RUN.verify_arguments()
    RUN.download_video()
