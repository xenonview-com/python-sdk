__title__ = 'xenon_view_sdk'
__version__ = '0.1.0'
__author__ = 'Xenon'
__copyright__ = 'Copyright 2021 Xenon'
'''
Created on September 20, 2021
@author: lwoydziak
'''
from datetime import datetime
from json import dumps
from time import sleep
from uuid import uuid4

import requests
from pytz import utc
from requests.api import post
from singleton3 import Singleton


class ApiException(Exception):
    def __init__(self, response, *args, **kwargs):
        super(ApiException, self).__init__(*args, **kwargs)
        self.__response = response

    def apiResponse(self):
        return self.__response


class Xenon(object, metaclass=Singleton):
    def __init__(self, apiKey=None, uuid=None, apiUrl='app.xenonview.com'):
        if not apiKey:
            raise ValueError('Xenon should be initialized with an API Key from XenonView.')
        self.__apiKey = apiKey
        self.__apiUrl = apiUrl
        self.__platform = None
        self.__tags = []
        self.__journey = []
        self.__id = str(uuid4()) if not uuid else uuid
        self.__restoreJourney = []

    def key(self, apiKey=None):
        if apiKey:
            self.__apiKey = apiKey
        return self.__apiKey

    # Platforming and Tagging:

    def platform(self, softwareVersion, deviceModel, operatingSystemName, operatingSystemVersion):
        platform = {
            'softwareVersion': softwareVersion,
            'deviceModel': deviceModel,
            'operatingSystemName': operatingSystemName,
            'operatingSystemVersion': operatingSystemVersion
        }
        self.__platform = platform

    def removePlatform(self):
        self.__platform = None

    def tag(self, tags):
        self.__tags = tags

    def untag(self):
        self.__tags = []

    # Stock Business Outcomes:

    def leadCaptured(self, specifier):
        content = {
            'superOutcome': 'Lead Capture',
            'outcome': specifier,
            'result': 'success'
        }
        self.outcomeAdd(content)

    def leadCaptureDeclined(self, specifier):
        content = {
            'superOutcome': 'Lead Capture',
            'outcome': specifier,
            'result': 'fail'
        }
        self.outcomeAdd(content)

    def accountSignup(self, specifier):
        content = {
            'superOutcome': 'Account Signup',
            'outcome': specifier,
            'result': 'success'
        }
        self.outcomeAdd(content)

    def accountSignupDeclined(self, specifier):
        content = {
            'superOutcome': 'Account Signup',
            'outcome': specifier,
            'result': 'fail'
        }
        self.outcomeAdd(content)

    def applicationInstalled(self):
        content = {
            'superOutcome': 'Application Installation',
            'outcome': 'Installed',
            'result': 'success'
        }
        self.outcomeAdd(content)

    def applicationNotInstalled(self):
        content = {
            'superOutcome': 'Application Installation',
            'outcome': 'Not Installed',
            'result': 'fail'
        }
        self.outcomeAdd(content)

    def initialSubscription(self, tier, method=None):
        content = {
            'superOutcome': 'Initial Subscription',
            'outcome': 'Subscribe - ' + tier,
            'result': 'success'
        }
        if method: content['method'] = method
        self.outcomeAdd(content)

    def subscriptionDeclined(self, tier, method=None):
        content = {
            'superOutcome': 'Initial Subscription',
            'outcome': 'Decline - ' + tier,
            'result': 'fail'
        }
        if method: content['method'] = method
        self.outcomeAdd(content)

    def subscriptionRenewed(self, tier, method=None):
        content = {
            'superOutcome': 'Subscription Renewal',
            'outcome': 'Renew - ' + tier,
            'result': 'success'
        }
        if method: content['method'] = method
        self.outcomeAdd(content)

    def subscriptionCanceled(self, tier, method=None):
        content = {
            'superOutcome': 'Subscription Renewal',
            'outcome': 'Cancel - ' + tier,
            'result': 'fail'
        }
        if method: content['method'] = method
        self.outcomeAdd(content)

    def subscriptionUpsold(self, tier, method=None):
        content = {
            'superOutcome': 'Subscription Upsold',
            'outcome': 'Upsold - ' + tier,
            'result': 'success'
        }
        if method: content['method'] = method
        self.outcomeAdd(content)

    def subscriptionUpsellDeclined(self, tier, method=None):
        content = {
            'superOutcome': 'Subscription Upsold',
            'outcome': 'Upsell Declined - ' + tier,
            'result': 'fail'
        }
        if method: content['method'] = method
        self.outcomeAdd(content)

    def referral(self, kind, detail=None):

        content = {
            'superOutcome': 'Referral',
            'outcome': 'Referred - ' + kind,
            'result': 'success'
        }
        if detail: content['details'] = detail

        self.outcomeAdd(content)

    def referralDeclined(self, kind, detail=None):
        content = {
            'superOutcome': 'Referral',
            'outcome': 'Referral Declined - ' + kind,
            'result': 'fail'
        }
        if detail: content['details'] = detail

        self.outcomeAdd(content)

    def productAddedToCart(self, product):
        content = {
            'superOutcome': 'Add Product To Cart',
            'outcome': 'Add - ' + product,
            'result': 'success'
        }
        self.outcomeAdd(content)

    def productNotAddedToCart(self, product):
        content = {
            'superOutcome': 'Add Product To Cart',
            'outcome': 'Ignore - ' + product,
            'result': 'fail'
        }
        self.outcomeAdd(content)

    def upsold(self, product):
        content = {
            'superOutcome': 'Upsold Product',
            'outcome': 'Upsold - ' + product,
            'result': 'success'
        }
        self.outcomeAdd(content)

    def upsellDismissed(self, product):
        content = {
            'superOutcome': 'Upsold Product',
            'outcome': 'Upsell Dismissed - ' + product,
            'result': 'fail'
        }
        self.outcomeAdd(content)

    def checkedOut(self):
        content = {
            'superOutcome': 'Customer Checkout',
            'outcome': 'Checked Out',
            'result': 'success'
        }
        self.outcomeAdd(content)

    def checkoutCanceled(self):
        content = {
            'superOutcome': 'Customer Checkout',
            'outcome': 'Checkout Canceled',
            'result': 'fail'
        }
        self.outcomeAdd(content)

    def productRemoved(self, product):
        content = {
            'superOutcome': 'Customer Checkout',
            'outcome': 'Product Removed - ' + product,
            'result': 'fail'
        }
        self.outcomeAdd(content)

    def purchased(self, method):
        content = {
            'superOutcome': 'Customer Purchase',
            'outcome': 'Purchase - ' + method,
            'result': 'success'
        }
        self.outcomeAdd(content)

    def purchaseCanceled(self, method=None):
        method = ' - ' + method if method else ''
        content = {
            'superOutcome': 'Customer Purchase',
            'outcome': 'Purchase Canceled' + method,
            'result': 'fail'
        }
        self.outcomeAdd(content)

    def promiseFulfilled(self):
        content = {
            'superOutcome': 'Promise Fulfillment',
            'outcome': 'Fulfilled',
            'result': 'success'
        }
        self.outcomeAdd(content)

    def promiseUnfulfilled(self):
        content = {
            'superOutcome': 'Promise Fulfillment',
            'outcome': 'Unfulfilled',
            'result': 'fail'
        }
        self.outcomeAdd(content)

    def productKept(self, product):
        content = {
            'superOutcome': 'Product Disposition',
            'outcome': 'Kept - ' + product,
            'result': 'success'
        }
        self.outcomeAdd(content)

    def productReturned(self, product):
        content = {
            'superOutcome': 'Product Disposition',
            'outcome': 'Returned - ' + product,
            'result': 'fail'
        }
        self.outcomeAdd(content)

    # Stock Milestones:

    def featureAttempted(self, name, detail=None):
        event = {
            'category': 'Feature',
            'action': 'Attempted',
            'name': name
        }
        if detail: event['details'] = detail
        self.journeyAdd(event)

    def featureCompleted(self, name, detail=None):
        event = {
            'category': 'Feature',
            'action': 'Completed',
            'name': name
        }
        if detail: event['details'] = detail
        self.journeyAdd(event)

    def featureFailed(self, name, detail=None):
        event = {
            'category': 'Feature',
            'action': 'Failed',
            'name': name
        }
        if detail: event['details'] = detail
        self.journeyAdd(event)

    def contentViewed(self, contentType, identifier=None):
        event = {
            'category': 'Content',
            'action': 'Viewed',
            'type': contentType,
        }
        if identifier: event['identifier'] = identifier
        self.journeyAdd(event)

    def contentEdited(self, contentType, identifier=None, detail=None):
        event = {
            'category': 'Content',
            'action': 'Edited',
            'type': contentType,
        }
        if identifier: event['identifier'] = identifier
        if detail: event['details'] = detail
        self.journeyAdd(event)

    def contentCreated(self, contentType, identifier=None):
        event = {
            'category': 'Content',
            'action': 'Created',
            'type': contentType,
        }
        if identifier: event['identifier'] = identifier
        self.journeyAdd(event)

    def contentDeleted(self, contentType, identifier=None):
        event = {
            'category': 'Content',
            'action': 'Deleted',
            'type': contentType,
        }
        if identifier: event['identifier'] = identifier
        self.journeyAdd(event)

    def contentRequested(self, contentType, identifier=None):
        event = {
            'category': 'Content',
            'action': 'Requested',
            'type': contentType,
        }
        if identifier: event['identifier'] = identifier
        self.journeyAdd(event)

    def contentSearched(self, contentType):
        event = {
            'category': 'Content',
            'action': 'Searched',
            'type': contentType,
        }
        self.journeyAdd(event)

    # Custom Milestones

    def milestone(self, category, operation, name, detail):
        event = {
            'category': category,
            'action': operation,
            'name': name,
            'details': detail
        }
        self.journeyAdd(event)

    # API Communication:

    def commit(self, PostMethod=post, sleepTime=1, verify=True):
        headers = {"Authorization": "Bearer " + self.__apiKey}
        journeyApi = {
            "name": "ApiJourney",
            "parameters": {
                "journey": self.journey(),
                "uuid": self.__id,
                "timestamp": datetime.now(utc).timestamp()
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

        self.__restoreJourney = []
        jsonResponse = response.json()
        return jsonResponse

    def heartbeat(self, PostMethod=post, sleepTime=1, verify=True):
        headers = {"Authorization": "Bearer " + self.__apiKey}

        parameters = {
            "journey": self.journey(),
            "uuid": self.__id,
            "timestamp": datetime.now(utc).timestamp()
        }

        if self.__platform: parameters["platform"] = self.__platform
        if len(self.__tags): parameters["tags"] = self.__tags

        heartbeatApi = {
            "name": "ApiHeartbeat",
            "parameters": parameters
        }
        response = None
        self.reset()
        for _ in range(3):
            try:
                path = 'https://' + self.__apiUrl + "/heartbeat"
                response = PostMethod(path, data=dumps(heartbeatApi), headers=headers, verify=verify)
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

        self.__restoreJourney = []
        jsonResponse = response.json()
        return jsonResponse

    def deanonymize(self, person, PostMethod=post, sleepTime=1, verify=True):
        headers = {"Authorization": "Bearer " + self.__apiKey}
        deanonymizeApi = {
            "name": "ApiDeanonymize",
            "parameters": {
                "person": person,
                "uuid": self.__id,
                "timestamp": datetime.now(utc).timestamp()
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

    # Internals:

    def id(self, _id=None):
        if _id:
            self.__id = _id
        return self.__id

    def newId(self):
        self.__id = str(uuid4())

    def outcomeAdd(self, content):
        if self.__platform: content['platform'] = self.__platform
        if len(self.__tags): content['tags'] = self.__tags
        self.journeyAdd(content)

    def journeyAdd(self, content):
        journey = self.journey()
        content['timestamp'] = datetime.now(utc).timestamp()
        if journey and len(journey) > 0:
            last = journey[-1]
            lastKeys = last.keys()
            contentKeys = content.keys()
            if ("funnel" in lastKeys and "funnel" in contentKeys) or (
                    "category" in lastKeys and "category" in contentKeys):
                if 'action' in lastKeys and \
                        'action' in contentKeys and \
                        last['action'] != content['action']:
                    journey.append(content)
                else:
                    count = last['count'] if 'count' in lastKeys else 1
                    last['count'] = count + 1
            else:
                journey.append(content)
        else:
            journey = [content]

        self.storeJourney(journey)

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

