'''
Created on September 20, 2021
@author: lwoydziak
'''
from mockito.matchers import Contains
from pytest import raises

from xenon_view_sdk import View


def setup_function(function):
    View._instance = None


def teardown_function(function):
    View._instance = None


def test_cannotCreateView():
    with raises(ValueError) as e:
        View()
    assert Contains('View should be initialized with an API Key from Xenon.').matches(str(e.exconly()))


def test_canChangeViewApiKey():
    View(apiKey='<API KEY>', apiUrl='<url>')
    newApiKey = 'new'
    View().key(newApiKey)
    assert newApiKey == View().key()
