# xenon-view-sdk

The Xenon View Python SDK is the Python SDK to interact with [XenonView](https://xenonview.com).

**Table of contents:**
* [What's New](#whats-new)
* [Installation](#installation)
* [How to use](#how-to-use)
* [License](#license)

## <a name="whats-new"></a>
## What's New
* v0.0.19 - Regenerate Journey ID with newId function.
* v0.0.18 - Add new platform method.
* v0.0.17 - Count duplicate steps instead of dropping them
* v0.0.16 - Rename View to Xenon
* v0.0.15 - Event adding follows standard
* v0.0.14 - Timestamp on commit
* v0.0.13 - Timestamps on every addition
* v0.0.12 - Can get and set a Journey ID
* v0.0.11 - Fully operational Outcome and Funnel methods
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
from xenon_view_sdk import Xenon

# start by initializing Xenon View
Xenon('<API KEY>')
```

-OR-

```python
from xenon_view_sdk import Xenon

# to initialize Xenon View after construction
Xenon('TBD')
Xenon().key('<API KEY>')
```

Of course, you'll have to make the following modifications to the above code:
- Replace `<API KEY>` with your [api key](https://xenonview.com/api-get)

### Platforming
After you have initialized View, you can optionally specify platform details such as:
- Operating System version
- Device model (Pixel, Docker Container, Linux VM, Dell Server, etc.)
- Software version of your application.

```python
from xenon_view_sdk import Xenon

softwareVersion = "5.1.5"
deviceModel = "Pixel 4 XL"
operatingSystemVersion = "Android 12.0"

# you can add platform details to outcomes
Xenon().platform(softwareVersion, deviceModel, operatingSystemVersion)
```
This adds platform details for each [outcome](#outcome). Typically, this would be set once at initialization:
```python
from xenon_view_sdk import Xenon

Xenon().key('<API KEY>')
softwareVersion = "5.1.5"
deviceModel = "Pixel 4 XL"
operatingSystemVersion = "Android 12.0"
Xenon().platform(softwareVersion, deviceModel, operatingSystemVersion)
```


### Add Journeys
After you have initialized the View singleton, you can start collecting journeys.

There are a few helper methods you can use:
#### <a name="outcome"></a>
#### Outcome
You can use this method to add an outcome to the journey.

```python
from xenon_view_sdk import Xenon

# you can add an outcome to journey
outcome = "<outcome>"
action = "<custom action>"
Xenon().outcome(outcome, action)
```
This adds an outcome to the journey chain effectively completing it.


#### Page view
You can use this method to add page views to the journey.

```python
from xenon_view_sdk import Xenon

# you can add a page view to a journey
page = 'test/page'
Xenon().pageView(page)
```
This adds a page view step to the journey chain.

#### Funnel Stage
You can use this method to track funnel stages in the journey.

```python
from xenon_view_sdk import Xenon

# you can add a funnel stage to a journey
action = "<custom action>"
stage = "<stage in funnel>"
Xenon().funnel(stage, action)
```
This adds a funnel stage to the journey chain.

#### Generic events
You can use this method to add generic events to the journey:

```python
from xenon_view_sdk import Xenon

# you can add a generic event to journey
event =  {
    'category': 'Event',
    'action': 'test'
}   
Xenon().event(event)
```
This adds an event step to the journey chain.

### Committing Journeys

Journeys only exist locally until you commit them to the Xenon View system. After you have created and added to a journey, you can commit the journey to Xenon View for analysis as follows:

```python
from xenon_view_sdk import Xenon

# you can commit a journey to Xenon View
Xenon().commit()
```
This commits a journey to Xenon View for analysis.

### Deanonymizing Journeys

Xenon View supports both anonymous and known journeys. By deanonymizing a journey you can compare a user's path to other known paths and gather insights into their progress. This is optional.

```python
from xenon_view_sdk import Xenon


def test_commitJourney():
person = {
    'name': 'Python Testing',
    'email': 'pytest@example.com'
}
# you can deanonymize before or after you have committed journey (in this case after):
Xenon().deanonymize(person)

# you can also deanonymize with a user ID:
person = {
    'UUID': "<some unique ID>"
}
Xenon().deanonymize(person)
```
This deanonymizes every journey committed to a particular user.

> **Note:** With journeys that span multiple platforms (eg. Website->Android->API backend), you can merge the journeys by deanonymizing on each platform.


### Journey IDs
Each Journey has an ID akin to a session. After an Outcome occurs the ID remains the same to link all the Journeys. If you have a previous Journey in progress and would like to append to that, you can set the ID.

> **Note:** For python, the Xenon object is a singleton. For multiple threads or async operations, the Journey ID will be reused.

After you have initialized the Xenon singleton, you can:
1. Use the default UUID
2. Set the Journey (Session) ID
3. Regenerate a new UUID

```python
from xenon_view_sdk import Xenon

# by default has Journey id
print(str(Xenon().id()))

# you can also set the id
testId = '<reuse previous ID>'
Xenon().id(testId)
assert Xenon().id() == testId

# lastly you can generate a new one (useful for serialized async operations that are for different customers)
Xenon().newId()
```

### Error handling
In the event of an API error, an exception will be raised with the response from the API as [Requests response object](https://docs.python-requests.org/en/latest/user/quickstart/#response-content):

>**Note:** The default handling of this situation will restore the journey (appending newly added pageViews, events, etc.) for future committing. If you want to do something special, you can do so like this:

```python
from xenon_view_sdk import Xenon, ApiException

try:
    Xenon().event({'step': 'a step in the journey'})
    Xenon().commit()

except ApiException as e:
    print(str(e.apiResponse().status_code))
```

## <a name="license"></a>
## License 

Apache Version 2.0

See [LICENSE](https://github.com/xenonview-com/view-python-sdk/blob/main/LICENSE)
