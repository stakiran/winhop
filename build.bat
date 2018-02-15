@echo off
python "%~dp0build.py" build
copy "%~dp0readme.md" "%~dp0winhop"
exit /b
