coverage run --source=selex -m unittest discover
coverage html
coverage report
coveralls