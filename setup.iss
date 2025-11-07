[Setup]
AppId={{12345678-1234-1234-1234-123456789012}
AppName=Custom Calculator
AppVersion=1.1.0
AppPublisher=Calc
DefaultDirName={autopf}\Custom Calculator
DefaultGroupName=Custom Calculator
OutputDir=Output
OutputBaseFilename=CustomCalculatortSetup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
UninstallDisplayIcon={app}\Calc.exe
SetupIconFile=icon.ico

[Icons]
Name: "{autoprograms}\Custom Calculator"; Filename: "{app}\Calc.exe"
Name: "{autodesktop}\Custom Calculator"; Filename: "{app}\Calc.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Создать значок на рабочем столе"; GroupDescription: "Дополнительные значки"

[Files]
Source: "Calc.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "history.json"; DestDir: "{app}"; Flags: ignoreversion
Source: ".env"; DestDir: "{app}"; Flags: ignoreversion
Source: "classes\*"; DestDir: "{app}\classes"; Flags: ignoreversion recursesubdirs
Source: "icons\*"; DestDir: "{app}\icons"; Flags: ignoreversion recursesubdirs

[Run]
Filename: "{app}\Calc.exe"; Description: "Запустить Custom Calculator"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}\history.json"
