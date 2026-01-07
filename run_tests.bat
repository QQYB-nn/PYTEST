@echo off
chcp 65001 > nul
echo [INFO] 正在启动测试...
REM 使用 python -m pytest 是关键，它能确保使用正确的Python环境
python -m pytest -v --tb=short
echo [INFO] 测试执行完毕。
if errorlevel 1 (
    echo [ERROR] 有测试用例失败！
    pause
)