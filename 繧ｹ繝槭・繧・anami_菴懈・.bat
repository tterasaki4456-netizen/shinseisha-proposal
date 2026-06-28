@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ===== 新生社様 提案ページ Nanami音声 埋め込み作成 =====
echo.
where python >nul 2>nul
if errorlevel 1 (
  echo [エラー] Python が見つかりません。
  echo https://www.python.org/downloads/ からインストールし、
  echo インストール画面で「Add Python to PATH」に必ずチェックを入れてください。
  echo その後、このファイルをもう一度ダブルクリックしてください。
  echo.
  pause
  exit /b 1
)
python build_nanami.py
echo.
echo 終了しました。出来上がった HTML を Netlify に公開してください。
pause
