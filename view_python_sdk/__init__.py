__title__ = 'view-python-sdk'
__version__ = '0.0.3'
__author__ = 'Xenon'
__copyright__ = 'Copyright 2021 Xenon'
'''
Created on September 20, 2021
@author: lwoydziak
'''
import requests

from json import dumps
from singleton3 import Singleton
from requests.api import post
from time import sleep


class View(object, metaclass=Singleton):
    def __init__(self, apiKey=None, apiUrl='app.xenonview.com'):
        if not apiKey:
            raise ValueError('View should be initialized with an API Key from Xenon.')
        self.__apiKey = apiKey
        self.__apiUrl = apiUrl

    def journey(self, journey, PostMethod=post, sleepTime=1, verify=True):
        headers = {"Authorization": "Bearer " + self.__apiKey}
        journeyApi = {
            "name": "ApiJourney",
            "parameters": {
                "journey": [journey]
            }
        }
        response = None
        for _ in range(3):
            try:
                path = 'https://' + self.__apiUrl + "/journey"
                response = PostMethod(path, data=dumps(journeyApi), headers=headers, verify=verify)
                break
            except requests.exceptions.SSLError as exception:
                sleep(sleepTime)
                continue
            except Exception as exception:
                sleep(sleepTime)
                continue

        if not response or not int(response.status_code) == 200:
            return None

        jsonResponse = response.json()
        return jsonResponse

    def journeys(self, PostMethod=post, sleepTime=1, verify=True):
        headers = {"Authorization": "Bearer " + self.__apiKey}
        journeysApi = {
            "name": "ApiJourneys",
            "parameters": {}
        }
        response = None
        for _ in range(3):
            try:
                path = 'https://' + self.__apiUrl + "/journeys"
                response = PostMethod(path, data=dumps(journeysApi), headers=headers, verify=verify)
                break
            except requests.exceptions.SSLError as exception:
                sleep(sleepTime)
                continue
            except Exception as exception:
                sleep(sleepTime)
                continue

        if not response or not int(response.status_code) == 200:
            return None

        jsonResponse = response.json()
        return jsonResponse
