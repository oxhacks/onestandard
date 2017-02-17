pipenv install
pytest --cov=onestandard --cov-report html:coverage
pylint onestandard
