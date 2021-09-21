'''
Created on September 20, 2021
@author: lwoydziak
'''
from mockito.matchers import any
from mockito.mocking import mock
from mockito.mockito import verify, when
from requests.exceptions import SSLError

from view_python_sdk import View

apiKey = '<apiKey>'
apiUrl = '<apiUrl>'


def setup_function(function):
    View(apiKey=apiKey, apiUrl=apiUrl)


def teardown_function(function):
    View._instance = None


def test_ApiGetJourneys():
    requests = mock()
    response = mock()
    response.status_code = 200
    when(requests).post('https://<apiUrl>/journeys', data=any(), headers=any(), verify=False).thenReturn(response)
    when(response).json().thenReturn({'journeys': []})
    View().journeys(PostMethod=requests.post, sleepTime=0, verify=False)
    verify(requests).post('https://<apiUrl>/journeys',
                          data=str('{"name": "ApiJourneys", "parameters": {}}'),
                          headers={'Authorization': 'Bearer <apiKey>'},
                          verify=False)


def test_ApiGetJourneysWithOneSslError():
    requests = mock()
    response = mock()
    response.status_code = 200
    when(requests).post('https://<apiUrl>/journeys', data=any(), headers=any(), verify=False).thenRaise(
        SSLError).thenReturn(response)
    when(response).json().thenReturn({'journeys': []})
    View().journeys(PostMethod=requests.post, sleepTime=0, verify=False)
    verify(requests, times=2).post('https://<apiUrl>/journeys',
                                   data=str('{"name": "ApiJourneys", "parameters": {}}'),
                                   headers={'Authorization': 'Bearer <apiKey>'},
                                   verify=False)


def test_ApiGetJourneysWithOneError():
    requests = mock()
    response = mock()
    response.status_code = 200
    when(requests).post('https://<apiUrl>/journeys', data=any(), headers=any(), verify=False).thenRaise(
        Exception).thenReturn(response)
    when(response).json().thenReturn({'journeys': []})
    View().journeys(PostMethod=requests.post, sleepTime=0, verify=False)
    verify(requests, times=2).post('https://<apiUrl>/journeys',
                                   data=str('{"name": "ApiJourneys", "parameters": {}}'),
                                   headers={'Authorization': 'Bearer <apiKey>'},
                                   verify=False)


def test_ApiGetJourneysFails():
    requests = mock()
    response = mock()
    response.status_code = 400
    when(requests).post('https://<apiUrl>/journeys', data=any(), headers=any(), verify=False).thenReturn(response)
    when(response).json().thenReturn({'result': 'failed'})
    assert not View().journeys(PostMethod=requests.post, sleepTime=0, verify=False)
