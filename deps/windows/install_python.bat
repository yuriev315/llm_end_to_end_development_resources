@echo off
rem Create an offline venv for one environment: install_python.bat <ENV>
rem Run from the package root (the folder that contains deps\ and windows\).
setlocal
set ENV=%1
if "%ENV%"=="" goto usage
if /I "%ENV%"=="A01" set PYV=3.10& set WH=deps\wheels\A01
if /I "%ENV%"=="A02" set PYV=3.10& set WH=deps\wheels\A02
if /I "%ENV%"=="A02_hf" set PYV=3.10& set WH=deps\wheels\A02_hf
if /I "%ENV%"=="A03" set PYV=3.10& set WH=deps\wheels\A03
if /I "%ENV%"=="A03_aider" set PYV=3.10& set WH=deps\wheels\A03_aider
if /I "%ENV%"=="A04" set PYV=3.10& set WH=deps\wheels\A04
if /I "%ENV%"=="A04_browser_use" set PYV=3.12& set WH=deps\wheels\A04_browser_use
if /I "%ENV%"=="A05_ag2" set PYV=3.10& set WH=deps\wheels\A05_ag2
if /I "%ENV%"=="A05_crewai" set PYV=3.10& set WH=deps\wheels\A05_crewai
if /I "%ENV%"=="REF_inspect_ai" set PYV=3.12& set WH=deps\wheels\REF_inspect_ai
if /I "%ENV%"=="REF_agentdojo" set PYV=3.10& set WH=deps\wheels\REF_agentdojo
if /I "%ENV%"=="REF_smolagents" set PYV=3.10& set WH=deps\wheels\REF_smolagents
if /I "%ENV%"=="REF_autogen" set PYV=3.10& set WH=deps\wheels\REF_autogen
if /I "%ENV%"=="REF_swebench" set PYV=3.10& set WH=deps\wheels\REF_swebench
if /I "%ENV%"=="REF_tau_bench" set PYV=3.10& set WH=deps\wheels\REF_tau_bench
if /I "%ENV%"=="REF_agentbench" set PYV=3.10& set WH=deps\wheels\REF_agentbench
if /I "%ENV%"=="REF_mcp_sdk" set PYV=3.10& set WH=deps\wheels\REF_mcp_sdk
if "%WH%"=="" goto usage
py -%PYV% -m venv venvs\%ENV% || goto fail
venvs\%ENV%\Scripts\python -m pip install --no-index --find-links "%WH%" -r deps\windows\pins\%ENV%.txt || goto fail
echo OK: venvs\%ENV%
goto end
:usage
echo usage: install_python.bat ^<ENV^>
echo ENV = A01 A02 A02_hf A03 A03_aider A04 A04_browser_use A05_ag2 A05_crewai REF_inspect_ai REF_agentdojo REF_smolagents REF_autogen REF_swebench REF_tau_bench REF_agentbench REF_mcp_sdk
exit /b 2
:fail
echo FAILED
exit /b 1
:end
endlocal
