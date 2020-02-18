@echo off

cd /D "%1"

FOR /F "delims=" %%i IN ('dir /b /ad-h /t:c /o-d') DO (
    SET a=%%~fi
    GOTO :found
)
echo No subfolder found
goto :eof
:found
echo Most recent subfolder: %a%

SET Quoted=%1
FOR /F "delims=" %%I IN (%Quoted%) DO SET Unquoted=%%I

@echo on
xcopy "%a%" "%Unquoted%/../../../Mesh" /s/y/E/i