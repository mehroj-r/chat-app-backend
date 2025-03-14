@echo off
for /f %%a in ('echo prompt $E^| cmd') do set "ESC=%%a"

:: Check for -build parameter
set REBUILD=false
for %%i in (%*) do (
    if /i "%%i"=="-build" set REBUILD=true
)

:: Rebuild images if -build parameter is passed
if "%REBUILD%"=="true" (
    echo %ESC%[0;33m[*] Rebuilding docker images ... %ESC%[0m
    docker-compose down
    docker-compose build --no-cache
    echo.
)

:: Initiate docker
echo %ESC%[0;31m[*] Initiating docker ... %ESC%[0m
docker-compose up -d
echo.

:: Make migration the db
echo %ESC%[0;31m[*] Migrating the database ... %ESC%[0m
docker-compose exec backend python manage.py makemigrations
echo.

:: Migrate the db
echo %ESC%[0;31m[*] Migrating the database ... %ESC%[0m
docker-compose exec backend python manage.py migrate
echo.