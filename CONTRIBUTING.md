# Development Environment

## Dependencies

* docker

## Running tests

You can run the tests for the whole project in the root directory by simply running:

```bash
./ant test
```
Note: you can run only a specific test by:  

```-Dtest=test_name```

##The following sections show how to run testing variants during development.

### Coverage

To run the tests in "coverage mode" (runs all tests then calculates coverage for each dir/file):
```bash
./ant coverage
```

# Publishing

_We (package maintainers) handle this step so this is more of internal notes:_

To publish the package (we standard pip packaging eg. setup.py and have scripts to automate):

```shell
./bump
./deploy deploy-prod
```
Note: you can also deploy-test to send to staging env.

# Contributing

We’d love to accept your patches and contributions to this project. Please review the following guidelines you'll need to follow in order to make a contribution.

## Contributor License Agreement

All contributors to this project must have a signed Contributor License Agreement (**"CLA"**) on file with us. The CLA grants us the permissions we need to use and redistribute your contributions as part of the project; you or your employer retain the copyright to your contribution. Head over to our website to see your current agreement(s) on file or to sign a new one.

We generally only need you (or your employer) to sign our CLA once and once signed, you should be able to submit contributions to any project.

Note: if you would like to submit an "_obvious fix_" for something like a typo, formatting issue or spelling mistake, you may not need to sign the CLA.

## Working on features

If you're interested on working on a feature for us we have a backlog, please contact us directly and we can find a good one.

## Code reviews

All submissions, including submissions by project members, require review and we use GitHub's pull requests for this purpose. Please consult [GitHub Help](https://help.github.com/articles/about-pull-requests/) if you need more information about using pull requests.
