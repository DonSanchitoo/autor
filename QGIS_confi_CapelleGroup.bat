@echo off
title Configuration de QGIS for Capelle Group : Autor

REM --- Variables
set "TARGET_DIR=%APPDATA%\QGIS\QGIS3"
set "CUSTOM_DIR=%APPDATA%\QGIS\QGIS3\profiles\default\QGIS"
set "LOGO_URL=https://raw.githubusercontent.com/DonSanchitoo/autor/main/logo.png"
set "STARTUP_URL=https://raw.githubusercontent.com/DonSanchitoo/autor/main/startup.py"
set "CUSTOM_URL=https://raw.githubusercontent.com/DonSanchitoo/autor/main/QGISCUSTOMIZATION3.ini"
set "TEMP_DIR=%TEMP%\autor_install_tmp"

REM --- Préparer les dossiers
if not exist "%TARGET_DIR%" (
    echo Création du dossier cible : "%TARGET_DIR%"
    mkdir "%TARGET_DIR%"
) else (
    echo Done
)

if not exist "%CUSTOM_DIR%" (
    echo Création du dossier personnalisation : "%CUSTOM_DIR%"
    mkdir "%CUSTOM_DIR%"
)

if not exist "%TEMP_DIR%" mkdir "%TEMP_DIR%"

powershell -NoProfile -Command "try { Invoke-WebRequest -Uri '%LOGO_URL%' -OutFile '%TEMP_DIR%\logo.png' -UseBasicParsing -ErrorAction Stop ; exit 0 } catch { exit 1 }"
if errorlevel 1 (
    echo Erreur 
) else (
    move /Y "%TEMP_DIR%\logo.png" "%TARGET_DIR%\" >nul
    echo Done
)

powershell -NoProfile -Command "try { Invoke-WebRequest -Uri '%STARTUP_URL%' -OutFile '%TEMP_DIR%\startup.py' -UseBasicParsing -ErrorAction Stop ; exit 0 } catch { exit 1 }"
if errorlevel 1 (
    echo Erreur : impossible de telecharger startup.py
) else (
    move /Y "%TEMP_DIR%\startup.py" "%TARGET_DIR%\" >nul
    echo Done
)

powershell -NoProfile -Command "try { Invoke-WebRequest -Uri '%CUSTOM_URL%' -OutFile '%TEMP_DIR%\QGISCUSTOMIZATION3.ini' -UseBasicParsing -ErrorAction Stop ; exit 0 } catch { exit 1 }"
if errorlevel 1 (
    echo Erreur : impossible de telecharger QGISCUSTOMIZATION3.ini
) else (
    move /Y "%TEMP_DIR%\QGISCUSTOMIZATION3.ini" "%CUSTOM_DIR%\" >nul
    echo Done
)

REM --- Nettoyage
if exist "%TEMP_DIR%" rd /s /q "%TEMP_DIR%"

echo.
echo Configuration terminee avec succes.
echo Appuyez sur une touche pour fermer...
pause >nul
exit /b 0
