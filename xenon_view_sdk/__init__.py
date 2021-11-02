__title__ = 'xenon_view_sdk'
__version__ = '0.0.9'
__author__ = 'Xenon'
__copyright__ = 'Copyright 2021 Xenon'
'''
Created on September 20, 2021
@author: lwoydziak
'''
from json import dumps
from time import sleep
from uuid import uuid4

import requests
from requests.api import post
from singleton3 import Singleton


class ApiException(Exception):
    def __init__(self, response, *args, **kwargs):
        super(ApiException, self).__init__(*args, **kwargs)
        self.__response = response

    def apiResponse(self):
        return self.__response


class View(object, metaclass=Singleton):
    def __init__(self, apiKey=None, uuid=None, apiUrl='app.xenonview.com'):
        if not apiKey:
            raise ValueError('View should be initialized with an API Key from Xenon.')
        self.__apiKey = apiKey
        self.__apiUrl = apiUrl
        self.__journey = []
        self.__id = str(uuid4()) if not uuid else uuid
        self.__restoreJourney = []

    def key(self, apiKey=None):
        if apiKey:
            self.__apiKey = apiKey
        return self.__apiKey

    def pageView(self, page):
        content = {
            'category': 'Page View',
            'action': page,
        }
        self.journeyAdd(content)

    def outcome(self, outcome, action):
        content = {
            'outcome': outcome,
            'action': action,
        }
        self.journeyAdd(content)

    def funnel(self, funnelStep, action):
        content = {
            'funnel': funnelStep,
            'action': action,
        }
        self.journeyAdd(content)

    def event(self, event):
        self.journeyAdd(event)

    def journeyAdd(self, content):
        journey = self.journey()
        if journey and len(journey) > 0:
            last = journey[-1]
            if last.keys() == content.keys():
                if 'action' in last.keys() and \
                   'action' in content.keys() and \
                   last['action'] != content['action']:
                    journey.append(content)
            else:
                journey.append(content)
        else:
            journey = [content]

        self.storeJourney(journey)

    def commit(self, PostMethod=post, sleepTime=1, verify=True):
        headers = {"Authorization": "Bearer " + self.__apiKey}
        journeyApi = {
            "name": "ApiJourney",
            "parameters": {
                "journey": self.journey(),
                "uuid": self.__id
            }
        }
        response = None
        self.reset()
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
            self.restore()
            raise ApiException(response, "Api responded with error.")

        jsonResponse = response.json()
        return jsonResponse

    def deanonymize(self, person, PostMethod=post, sleepTime=1, verify=True):
        headers = {"Authorization": "Bearer " + self.__apiKey}
        deanonymizeApi = {
            "name": "ApiDeanonymize",
            "parameters": {
                "person": person,
                "uuid": self.__id
            }
        }
        response = None
        for _ in range(3):
            try:
                path = 'https://' + self.__apiUrl + "/deanonymize"
                response = PostMethod(path, data=dumps(deanonymizeApi), headers=headers, verify=verify)
                break
            except requests.exceptions.SSLError as exception:
                sleep(sleepTime)
                continue
            except Exception as exception:
                sleep(sleepTime)
                continue

        if not response or not int(response.status_code) == 200:
            raise ApiException(response, "Api responded with error.")

        jsonResponse = response.json()
        return jsonResponse

    def journeys(self, PostMethod=post, sleepTime=1, verify=True):
        headers = {"Authorization": "Bearer " + self.__apiKey}
        journeysApi = {
            "name": "ApiJourneys",
            "parameters": {"uuid": self.__id}
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
            raise ApiException(response, "Api responded with error.")

        jsonResponse = response.json()
        return jsonResponse

    def journey(self):
        return self.__journey

    def storeJourney(self, journey):
        self.__journey = journey

    def reset(self):
        self.__restoreJourney = self.journey()
        self.__journey = []

    def restore(self):
        currentJourney = self.journey()
        restoreJourney = self.__restoreJourney
        if currentJourney and len(currentJourney) > 0:
            restoreJourney.extend(currentJourney)
        self.storeJourney(restoreJourney)
        self.__restoreJourney = []
