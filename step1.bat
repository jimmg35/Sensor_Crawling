@echo off
REM Author : jimmg35
REM compatible with python version 3.5 or higher.
REM performing static type check before execution.
REM step1 postgres jim60308 localhost 5432

cd dbcontext
python create.py %1 %2 %3 %4
cd ..
python injectdata.py