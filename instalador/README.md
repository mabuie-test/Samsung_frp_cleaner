# Instalador do FRP Cleaner Samsung

Esta pasta contém os artefactos necessários para gerar um instalador Windows (.exe) tradicional a partir do executável standalone produzido pelo PyInstaller.

## Estrutura

- `build_installer.ps1` — script PowerShell que automatiza a geração do executável com o PyInstaller, prepara a pasta `staging/` e invoca o Inno Setup reutilizando automaticamente a versão definida em `cleaner.__version__`.
- `frp_cleaner_installer.iss` — script do Inno Setup responsável por empacotar o executável e arquivos auxiliares num instalador gráfico.
- `resources/README_instalacao.txt` — texto exibido ao final da instalação com um guia rápido.

A pasta `staging/` será criada dinamicamente pelo script PowerShell e não deve ser versionada; nela ficam os ficheiros temporários copiados para o instalador.

## Pré-requisitos no Windows

1. Python 3.10+ com as dependências listadas em `requesitos.txt` (instale-as dentro de uma `venv`).
2. PyInstaller (já incluído em `requesitos.txt`).
3. [Inno Setup](https://jrsoftware.org/isinfo.php) instalado e o comando `iscc.exe` disponível no `PATH`.

## Fluxo recomendado

1. Abra um terminal PowerShell na raiz do repositório clonado no Windows.
2. Ative a sua `venv` e instale as dependências (`pip install -r requesitos.txt`).
3. Execute o script:
   ```powershell
   ./instalador/build_installer.ps1
   ```
4. Ao final, o instalador `FRP_Cleaner_Setup.exe` será gerado na pasta `instalador/dist/`.

Caso prefira chamar as etapas manualmente:

1. Gere o executável standalone com `python build_windows_exe.py`.
2. Copie `dist/FRP-Cleaner.exe` e `instalador/resources/README_instalacao.txt` para `instalador/staging/`.
3. Compile o script `frp_cleaner_installer.iss` com o Inno Setup (`iscc instalador/frp_cleaner_installer.iss`).

> **Nota:** tanto o executável quanto o instalador dependem da configuração do WSL e das ferramentas externas indicadas no README principal.
