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


def test_canAddPageView():
    View(apiKey='<API KEY>')
    View().pageView("mine")
    assert View().journey() == [{'category': 'Page View', 'action': 'mine'}]


def test_canAddOutcome():
    View(apiKey='<API KEY>')
    View().outcome("<my outcome>", "<action>")
    assert View().journey() == [{'outcome': '<my outcome>', 'action': '<action>'}]


def test_canAddFunnel():
    View(apiKey='<API KEY>')
    View().funnel("<my step in funnel>", "<action>")
    assert View().journey() == [{'funnel': '<my step in funnel>', 'action': '<action>'}]


def test_doesNotAddDuplicateEvent():
    View(apiKey='<API KEY>')
    View().event({'e1': 'event1'})
    View().event({'e1': 'event1'})
    assert View().journey() == [{'e1': 'event1'}]


def test_addSecondEvent():
    View(apiKey='<API KEY>')
    View().event({'e1': 'event1'})
    View().event({'e2': 'event2'})
    assert View().journey() == [{'e1': 'event1'}, {'e2': 'event2'}]


def test_addSecondPageView():
    View(apiKey='<API KEY>')
    View().pageView('p1')
    View().pageView('p2')
    assert View().journey() == [
        {'action': 'p1', 'category': 'Page View'},
        {'action': 'p2', 'category': 'Page View'}
    ]


def test_whenResetingAddingEventAndRestoringRestoredJourneyHasNewEvent():
    View(apiKey='<API KEY>')
    View().event({'e1': 'event1'})
    View().reset()
    View().event({'e2': 'event2'})
    View().restore()
    assert View().journey() == [{'e1': 'event1'}, {'e2': 'event2'}]


def test_canGetAndSetId():
    View(apiKey='<API KEY>')
    assert View().id() != None and View().id() != ''
    View().id('test')
    assert View().id() == 'test'
