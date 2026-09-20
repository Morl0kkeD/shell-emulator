@echo off
chcp 65001 > nul
echo === Запуск эмулятора со скриптом Stage 5 ===
python src/main.py --vfs vfs_examples/medium.xml --script scripts/test_stage5.txt

echo.
echo === Запуск эмулятора в графическом режиме (GUI) ===
python src/main.py --vfs vfs_examples/medium.xml
pause