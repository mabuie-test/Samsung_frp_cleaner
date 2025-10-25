#define MyAppName "FRP Cleaner Samsung"
#ifndef MyAppVersion
#define MyAppVersion "1.0.0"
#endif
#define MyAppPublisher "Mestre Jorge Augusto Mabuie"
#define MyAppExeName "FRP-Cleaner.exe"

[Setup]
AppId={{0FB3E325-0861-45E4-A4B2-9E4E3A53B4BE}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\FRP Cleaner Samsung
DefaultGroupName=FRP Cleaner Samsung
OutputBaseFilename=FRP_Cleaner_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64
ChangesAssociations=yes
DisableProgramGroupPage=yes

[Languages]
Name: "portugues"; MessagesFile: "compiler:Languages\Portuguese.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na área de trabalho"; GroupDescription: "Opções adicionais:"; Flags: unchecked

[Files]
Source: "{#SourcePath}staging\FRP-Cleaner.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SourcePath}staging\README_instalacao.txt"; DestDir: "{app}"; Flags: isreadme

[Icons]
Name: "{autoprograms}\FRP Cleaner Samsung"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\FRP Cleaner Samsung"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Executar o FRP Cleaner agora"; Flags: nowait postinstall skipifsilent
