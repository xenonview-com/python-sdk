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
    journey = View().journey()[0]
    assert journey['category'] == 'Page View'
    assert journey['action'] == 'mine'
    assert journey['timestamp'] > 0.0



def test_canAddOutcome():
    View(apiKey='<API KEY>')
    View().outcome("<my outcome>", "<action>")
    journey = View().journey()[0]
    assert journey['outcome'] == '<my outcome>'
    assert journey['action'] == '<action>'
    assert journey['timestamp'] > 0.0

def test_canAddFunnel():
    View(apiKey='<API KEY>')
    View().funnel("<my step in funnel>", "<action>")
    journey = View().journey()[0]
    assert journey['funnel'] == '<my step in funnel>'
    assert journey['action'] == '<action>'
    assert journey['timestamp'] > 0.0


def test_doesNotAddDuplicateEvent():
    View(apiKey='<API KEY>')
    View().event({'e1': 'event1'})
    View().event({'e1': 'event1'})
    journey = View().journey()[0]
    assert journey['e1'] == 'event1'
    assert journey['timestamp'] > 0.0

def test_addSecondEvent():
    View(apiKey='<API KEY>')
    View().event({'e1': 'event1'})
    View().event({'e2': 'event2'})
    journey = View().journey()[0]
    assert journey['e1'] == 'event1'
    assert journey['timestamp'] > 0.0
    journey = View().journey()[1]
    assert journey['e2'] == 'event2'
    assert journey['timestamp'] > 0.0


def test_addSecondPageView():
    View(apiKey='<API KEY>')
    View().pageView('p1')
    View().pageView('p2')

    journey = View().journey()[0]
    assert journey['category'] == 'Page View'
    assert journey['action'] == 'p1'
    assert journey['timestamp'] > 0.0
    journey = View().journey()[1]
    assert journey['category'] == 'Page View'
    assert journey['action'] == 'p2'
    assert journey['timestamp'] > 0.0


def test_whenResetingAddingEventAndRestoringRestoredJourneyHasNewEvent():
    View(apiKey='<API KEY>')
    View().event({'e1': 'event1'})
    View().reset()
    View().event({'e2': 'event2'})
    View().restore()
    journey = View().journey()[0]
    assert journey['e1'] == 'event1'
    assert journey['timestamp'] > 0.0
    journey = View().journey()[1]
    assert journey['e2'] == 'event2'
    assert journey['timestamp'] > 0.0


def test_canGetAndSetId():
    View(apiKey='<API KEY>')
    assert View().id() != None and View().id() != ''
    View().id('test')
    assert View().id() == 'test'
