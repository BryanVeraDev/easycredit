@echo off

rem Define the commands for each action
set COMMAND_RUN=python manage.py runserver --settings=creditoapp.settings.local
set COMMAND_TEST=python manage.py test --settings=creditoapp.settings.local
set COMMAND_LINT=ruff check
set COMMAND_COVERAGE=coverage run --source='.\' manage.py test --settings=creditoapp.settings.local ^&^& coverage report
rem Check the first argument (the action to perform)
if "%1" == "run" (
    %COMMAND_RUN%
) else if "%1" == "test" (
    %COMMAND_TEST%
) else if "%1" == "lint" (
    %COMMAND_LINT%
) else if "%1" == "coverage" (
    %COMMAND_COVERAGE%
) else (
    echo Invalid command. Use 'run', 'test', 'lint', or 'coverage'.
)