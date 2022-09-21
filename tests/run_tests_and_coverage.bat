coverage run --source=selex -m unittest discover
@REM Skip report generation and coveralls if tests failed
if not %ERRORLEVEL%==0 GOTO :EOF
coverage html
coverage report
coveralls