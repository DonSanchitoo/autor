@echo off
title Configuration de QGIS for Capelle Group : Autor

REM --- Variables
set "TARGET_DIR=%APPDATA%\QGIS\QGIS3"
set "LOGO_URL=https://raw.githubusercontent.com/DonSanchitoo/autor/main/logo.png"
set "STARTUP_URL=https://raw.githubusercontent.com/DonSanchitoo/autor/main/startup.py"
set "TEMP_DIR=%TEMP%\autor_install_tmp"

REM --- Préparer les dossiers
if not exist "%TARGET_DIR%" (
    echo Création du dossier cible : "%TARGET_DIR%"
    mkdir "%TARGET_DIR%"
) else (
    echo Dossier cible existe : "%TARGET_DIR%"
)

if not exist "%TEMP_DIR%" mkdir "%TEMP_DIR%"

powershell -NoProfile -Command "try { Invoke-WebRequest -Uri '%LOGO_URL%' -OutFile '%TEMP_DIR%\logo.png' -UseBasicParsing -ErrorAction Stop ; exit 0 } catch { exit 1 }"
if errorlevel 1 (
    echo Erreur : impossible de telecharger logo.png
) else (
    move /Y "%TEMP_DIR%\logo.png" "%TARGET_DIR%\" >nul
    echo logo.png placé dans "%TARGET_DIR%"
)

powershell -NoProfile -Command "try { Invoke-WebRequest -Uri '%STARTUP_URL%' -OutFile '%TEMP_DIR%\startup.py' -UseBasicParsing -ErrorAction Stop ; exit 0 } catch { exit 1 }"
if errorlevel 1 (
    echo Erreur : impossible de telecharger startup.py
) else (
    move /Y "%TEMP_DIR%\startup.py" "%TARGET_DIR%\" >nul
    echo startup.py placé dans "%TARGET_DIR%"
)

REM --- Nettoyage
if exist "%TEMP_DIR%" rd /s /q "%TEMP_DIR%"

echo.
echo Configuration terminee avec succes.
echo Appuyez sur une touche pour fermer...
pause >nul
exit /b 0