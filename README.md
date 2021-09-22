# view-python-sdk

The View Python SDK is the Python SDL to interact with [XenonView](https://xenonview.com).

**Table of contents:**

* [Installation](#installation)
* [How to use](#how-to-use)
* [License](#license)

## <a name="installation"></a>
## Installation

You can install the View Python SDK from [PyPI](https://pypi.org/project/realpython-reader/):

```bash
    pip install view-python-sdk
```

The SDK is supported on Python 3+.

## <a name="how-to-use"></a>
## How to use

### Instantiation
The View SDK is a Python module you'll need to include in your application. After inclusion, you'll need to instantiate the singleton object:

```python
    from view_python_sdk import View


    def test_createView():
        View('<API KEY>')
```
Of course, you'll have to make the following modifications to the above code:
- Replace `<API KEY>` with your [api key](https://xenonview.com/api-get)

### Add Journeys
After you have initialized the View singleton, you can start collecting journeys:

```python
    from view_python_sdk import View


    def test_addJourney():
        email = 'test@test.com'
        View('<API KEY>')
        View().journey([
            {
                'category': 'Page View',
                'action': 'Landing page (/sign-up)'
            },
            {
                'category': 'Submit',
                'action': 'Submit (/sign-up) email: ' + email,
                'label': 'submit-email'    
            }
        ])
```
This adds a journey to the journey chain. 

### View Journeys
After you have initialized the View singleton, you can also view journeys:

```python
    from view_python_sdk import View


    def test_viewJourneys():
        View('<API KEY>')
        print(str(View().journeys()))
```

### Delayed setting of the API Key
Optionally you can set the API Key later:

```python
    from view_python_sdk import View


    def test_createView():
        View('TBD')
        View().setKey('<API KEY>')
```

## <a name="license"></a>
## License 

Apache Version 2.0

See [LICENSE](https://github.com/xenonview-com/view-python-sdk/blob/main/LICENSE)
