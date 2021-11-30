'''
Created on September 20, 2021
@author: lwoydziak
'''
from mockito.matchers import any, Contains, And
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
    View().event({'step': 'step1'})
    View().commit(PostMethod=requests.post, sleepTime=0, verify=False)
    verify(requests).post('https://<apiUrl>/journey',
                          data=And([Contains('{"name": "ApiJourney", "parameters": '),
                                    Contains('{"journey": [{"step": "step1", "timestamp":'),
                                    Contains('}], "uuid":')]),
                          headers={'Authorization': 'Bearer <apiKey>'},
                          verify=False)
    assert View().journey() == []


def test_viewJourneyFailsWithOneSslError():
    requests = mock()
    response = mock()
    response.status_code = 200
    when(requests).post('https://<apiUrl>/journey', data=any(), headers=any(), verify=False).thenRaise(
        SSLError).thenReturn(response)
    when(response).json().thenReturn({'result': 'success'})
    View().event({'step': 'step1'})
    View().commit(PostMethod=requests.post, sleepTime=0, verify=False)
    verify(requests, times=2).post('https://<apiUrl>/journey',
                                   data=And([Contains('{"name": "ApiJourney", "parameters": '),
                                             Contains('{"journey": [{"step": "step1", "timestamp":'),
                                             Contains('}], "uuid":')]),
                                   headers={'Authorization': 'Bearer <apiKey>'},
                                   verify=False)
    assert View().journey() == []


def test_viewJourneyFailsWithOneError():
    requests = mock()
    response = mock()
    response.status_code = 200
    when(requests).post('https://<apiUrl>/journey', data=any(), headers=any(), verify=False).thenRaise(
        Exception).thenReturn(response)
    when(response).json().thenReturn({'result': 'success'})
    View().event({'step': 'step1'})
    View().commit(PostMethod=requests.post, sleepTime=0, verify=False)
    verify(requests, times=2).post('https://<apiUrl>/journey',
                                   data=And([Contains('{"name": "ApiJourney", "parameters": '),
                                             Contains('{"journey": [{"step": "step1", "timestamp":'),
                                             Contains('}], "uuid":')]),
                                   headers={'Authorization': 'Bearer <apiKey>'},
                                   verify=False)
    assert View().journey() == []


def test_viewJourneyFails():
    requests = mock()
    response = mock()
    response.status_code = 400
    when(requests).post('https://<apiUrl>/journey', data=any(), headers=any(), verify=False).thenReturn(response)
    when(response).json().thenReturn({'result': 'failed'})
    with raises(ApiException) as e:
        View().event({'step': 'step1'})
        View().commit(PostMethod=requests.post, sleepTime=0, verify=False)

    assert Contains('Api responded with error.').matches(str(e.exconly()))
    journey = View().journey()[0]
    assert journey['step'] == 'step1'
    assert journey['timestamp'] > 0.0


def test_WhenViewJourneyFailsExceptionContainsResponse():
    requests = mock()
    response = mock()
    response.status_code = 400
    when(requests).post('https://<apiUrl>/journey', data=any(), headers=any(), verify=False).thenReturn(response)
    when(response).json().thenReturn({'result': 'failed'})
    try:
        View().event({'step': 'step1'})
        View().commit(PostMethod=requests.post, sleepTime=0, verify=False)
    except ApiException as e:
        assert e.apiResponse().status_code == response.status_code
