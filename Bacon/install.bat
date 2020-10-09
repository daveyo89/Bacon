>nul 2>nul assoc .py
if exist %systemdrive%%homepath%\Cypher\Cypher.exe (
    cls
    echo "Program already installed.. "
    pause
) else (
    if errorlevel 1 (
        echo Not available
        @"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
        choco install -y python3
    )
    python --version
    python3 -m venv .\venv
    call .\venv\Scripts\activate.bat
    call pip install -r requirements.txt
    pyinstaller --name Cypher --console --onefile --clean --distpath %systemdrive%%homepath%\Cypher --icon icon.ico  --windowed main.py
    copy icon.ico %systemdrive%%homepath%\Cypher\
    copy config.yml %systemdrive%%homepath%\Cypher\
    rd /s/q "build"
    rd /s/q "__pycache__"
    del Cypher.spec
)