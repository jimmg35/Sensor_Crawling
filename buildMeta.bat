@echo off
REM Author : jimmg35
REM compatible with python version 3.5 or higher.
REM performing static type check before execution.
REM build postgres jim60308 localhost 5432
REM ==============================================
REM %1 : database user id
REM %2 : password
REM %3 : hostname
REM %4 : port
REM ==============================================
cd dbcontext
python createMeta.py %1 %2 %3 %4
cd ..
python injectmeta.py