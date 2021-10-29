# xenon-view-sdk

The Xenon View Python SDK is the Python SDK to interact with [XenonView](https://xenonview.com).

**Table of contents:**
* [What's New](#whats-new)
* [Installation](#installation)
* [How to use](#how-to-use)
* [License](#license)

## <a name="whats-new"></a>
## What's New
* v0.0.7 - Fully operational deanonymization
* v0.0.4 - User error handling supported
* v0.0.2 - Basic Functionality

## <a name="installation"></a>
## Installation

You can install the View Python SDK from [PyPI](https://pypi.org/project/xenon-view-sdk):

```bash
    pip install xenon-view-sdk
```

The SDK is supported on Python 3+.

## <a name="how-to-use"></a>
## How to use

The Xenon View SDK can be used in your application to provide a whole new level of user analysis and insights. You'll need to embed the instrumentation into your application via this SDK. The basic operation is to create a customer journey by adding steps in the journey like page views, funnel steps and other events. The journey concludes with an outcome. All of this can be committed for analysis on your behalf to Xenon View. From there you can see popular journeys that result in both successful an unsuccessful outcomes. Additionally, you can deanonymize journeys. This will allow for a deeper analysis of a particular user. This is an optional step as just tracking which journey results in what outcome is valuable.   

### Instantiation
The View SDK is a Python module you'll need to include in your application. After inclusion, you'll need to instantiate the singleton object:

```python
from xenon_view_sdk import View


def test_createView():
    View('<API KEY>')
```
Of course, you'll have to make the following modifications to the above code:
- Replace `<API KEY>` with your [api key](https://xenonview.com/api-get)

Optionally you can set the API Key later:

```python
from xenon_view_sdk import View


def test_createView():
    View('TBD')
    View().key('<API KEY>')
```

### Add Journeys
After you have initialized the View singleton, you can start collecting journeys.

There are a few helper methods you can use:

#### Page view
You can use this method to add page views to the journey.
```python
from xenon_view_sdk import View


def test_addPageView():
    page = 'test/page'
    View('<API KEY>')
    View().pageView(page)
```
This adds a page view step to the journey chain.


#### Generic events
You can use this method to add generic events to the journey:

```python
from xenon_view_sdk import View


def test_addEvent():
    email = 'test@test.com'
    View('<API KEY>')
    View().event({
            'category': 'Submit',
            'action': 'Submit (/sign-up) email: ' + email,
            'label': 'submit-email'
        })
```
This adds an event step to the journey chain.

### Committing Journeys

Journeys only exist locally until you commit them to the Xenon View system. After you have created and added to a journey, you can commit the journey to Xenon View for analysis as follows:
```python
from xenon_view_sdk import View


def test_commitJourney():
    email = 'test@test.com'
    View('<API KEY>')
    # <add some steps in the journey>
    # commit
    View().commit()
```
This commits a journey to Xenon View for analysis.

### Deanonymizing Journeys

Xenon View supports both anonymous and known journeys. By deanonymizing a journey you can compare a user's path to other known paths and gather insights into their progress. This is optional.
```python
from xenon_view_sdk import View


def test_commitJourney():
    name = 'Python Testing'
    email = 'pytest@example.com'
    View('<API KEY>')
    # <add some steps in the journey>
    # <commit>
    # you can deanonymize before or after you have committed journey (in this case after):
    View().deanonymize({'name': name, 'email':email})
```
This deanonymizes every journey committed to a particular user.


### View Journeys
After you have initialized the View singleton, you can also view journeys:

```python
from xenon_view_sdk import View


def test_viewJourneys():
    View('<API KEY>')
    print(str(View().journeys()))
```

### Error handling
In the event of an API error, an exception will be raised with the response from the API as [Requests response object](https://docs.python-requests.org/en/latest/user/quickstart/#response-content):

Note: The default handling of this situation will restore the journey (appending newly added pageViews, events, etc.) for future committing. If you want to do something special, you can do so like this:

```python
from xenon_view_sdk import View, ApiException

try:
    View().event({'step': 'a step in the journey'})
    View().commit()
    
except ApiException as e:
    print(str(e.apiResponse().status_code))
```

## <a name="license"></a>
## License 

Apache Version 2.0

See [LICENSE](https://github.com/xenonview-com/view-python-sdk/blob/main/LICENSE)
