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


def test_viewJourneyAdded():
    requests = mock()
    response = mock()
    response.status_code = 200
    when(requests).post('https://<apiUrl>/journey', data=any(), headers=any(), verify=False).thenReturn(response)
    when(response).json().thenReturn({'result': 'success'})
    View().journey({'step': 'step1'}, PostMethod=requests.post, sleepTime=0, verify=False)
    verify(requests).post('https://<apiUrl>/journey',
                          data=str('{"name": "ApiJourney", "parameters": '
                                   '{"journey": [{"step": "step1"}]}}'),
                          headers={'Authorization': 'Bearer <apiKey>'},
                          verify=False)


def test_viewJourneyFailsWithOneSslError():
    requests = mock()
    response = mock()
    response.status_code = 200
    when(requests).post('https://<apiUrl>/journey', data=any(), headers=any(), verify=False).thenRaise(
        SSLError).thenReturn(response)
    when(response).json().thenReturn({'result': 'success'})
    View().journey({'step': 'step1'}, PostMethod=requests.post, sleepTime=0, verify=False)
    verify(requests, times=2).post('https://<apiUrl>/journey',
                                   data=str('{"name": "ApiJourney", "parameters": '
                                            '{"journey": [{"step": "step1"}]}}'),
                                   headers={'Authorization': 'Bearer <apiKey>'},
                                   verify=False)


def test_viewJourneyFailsWithOneError():
    requests = mock()
    response = mock()
    response.status_code = 200
    when(requests).post('https://<apiUrl>/journey', data=any(), headers=any(), verify=False).thenRaise(
        Exception).thenReturn(response)
    when(response).json().thenReturn({'result': 'success'})
    View().journey({'step': 'step1'}, PostMethod=requests.post, sleepTime=0, verify=False)
    verify(requests, times=2).post('https://<apiUrl>/journey',
                                   data=str('{"name": "ApiJourney", "parameters": '
                                            '{"journey": [{"step": "step1"}]}}'),
                                   headers={'Authorization': 'Bearer <apiKey>'},
                                   verify=False)


def test_viewJourneyFails():
    requests = mock()
    response = mock()
    response.status_code = 400
    when(requests).post('https://<apiUrl>/journey', data=any(), headers=any(), verify=False).thenReturn(response)
    when(response).json().thenReturn({'result': 'failed'})
    assert not View().journey({'step': 'step1'}, PostMethod=requests.post, sleepTime=0, verify=False)
