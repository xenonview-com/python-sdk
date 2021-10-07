'''
Created on September 20, 2021
@author: lwoydziak
'''
from mockito.matchers import any, Contains
from mockito.mocking import mock
from mockito.mockito import verify, when
from pytest import raises
from requests.exceptions import SSLError

from xenon_view_sdk import View, ApiException

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
    View().journey([{'step': 'step1'}], PostMethod=requests.post, sleepTime=0, verify=False)
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
    View().journey([{'step': 'step1'}], PostMethod=requests.post, sleepTime=0, verify=False)
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
    View().journey([{'step': 'step1'}], PostMethod=requests.post, sleepTime=0, verify=False)
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
    with raises(ApiException) as e:
        View().journey({'step': 'step1'}, PostMethod=requests.post, sleepTime=0, verify=False)

    assert Contains('Api responded with error.').matches(str(e.exconly()))


def test_WhenViewJourneyFailsExceptionContainsResponse():
    requests = mock()
    response = mock()
    response.status_code = 400
    when(requests).post('https://<apiUrl>/journey', data=any(), headers=any(), verify=False).thenReturn(response)
    when(response).json().thenReturn({'result': 'failed'})
    try:
        View().journey({'step': 'step1'}, PostMethod=requests.post, sleepTime=0, verify=False)
    except ApiException as e:
        assert e.apiResponse().status_code == response.status_code
