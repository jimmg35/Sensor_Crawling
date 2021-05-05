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
REM %5 : start year
REM %6 : start month
REM %7 : start day
REM %8 : end year
REM %9 : end month
REM %10 : end day
REM ==============================================
cd dbcontext
python createFixed.py %1 %2 %3 %4 %5 %6 %9
cd ..
set list[0]=%1
SHIFT
python FixedData.py %list[0]% %1 %2 %3 %4 %5 %6 %7 %8 %9



REM deviceid, 年月日, 小時, 分, 秒, 