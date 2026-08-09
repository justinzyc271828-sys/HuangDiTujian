@echo off
chcp 65001 >nul
title 皇帝图鉴 · 本地预览（关闭本窗口即停止服务）
cd /d %~dp0apps\web
start "" powershell -WindowStyle Hidden -Command "$i=0; while($i -lt 90){ try { $r = Invoke-WebRequest -UseBasicParsing http://localhost:5173/ -TimeoutSec 1; if ($r.StatusCode -eq 200) { break } } catch { }; Start-Sleep -Milliseconds 500; $i++ }; Start-Process http://localhost:5173/"
echo 正在启动本地预览，浏览器会自动打开...
echo 看完直接关闭本窗口即可停止服务。
npm run dev
