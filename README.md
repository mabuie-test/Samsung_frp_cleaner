# Samsung_frp_cleaner

> **FRP Cleaner Samsung (Windows + WSL)**
>
> Ferramenta avançada, modular e didáctica, desenvolvida em Python, destinada a remover o mecanismo de Protecção de Reinicialização de Fábrica (FRP – Factory Reset Protection) de ROMs Samsung. Através da integração cuidadosa de técnicas de engenharia reversa e patching de segurança, esta aplicação permite ao utilizador — sempre em contexto de manutenção autorizada ou recuperação forense — preparar um pacote de firmware limpo, pronto para flash via Odin, sem recusa por parte do bootloader.
>
> **Funcionalidades principais:**
>
> 1. **Conversão de Imagens**: Transforma, quando necessário, imagens ‘sparse’ em raw (`sparse.img` → `system_raw.img`), assegurando compatibilidade total com ferramentas Linux.
> 2. **Montagem e Limpeza FRP**: Monta automaticamente a partição `system.img` em ambiente WSL, detecta e neutraliza componentes ligados ao FRP (SetupWizard, FRPHandler, scripts de verificação), preservando integridade através de renomeação ou remoção controlada.
> 3. **Patch AVB (Android Verified Boot)**: Utiliza o `avbtool` para gerar um `vbmeta.img` com flags de verificação e árvore de hashes desativadas, evitando rejeição por parte do bootloader.
> 4. **Bypass dm‑verity**: Emprega o `magiskboot` para patch do `boot.img`, injetando os mecanismos necessários ao arranque com sistema de ficheiros modificado.
> 5. **Reempacotamento e MD5**: Gera um único pacote `.tar.md5` plenamente válido para o Odin, recriando o artefacto de forma idêntica ao original, mas sem o FRP.
> 6. **Logging e Auditoria**: Regista, em detalhe, todas as operações — desde a conversão até ao patching e reempacotamento — num ficheiro de log estruturado, garantindo total rastreabilidade.
>
> **Arquitetura e extesibilidade:**
> A estrutura do projecto foi elaborada com separação de responsabilidades em módulos (`img_manager`, `frp_detector`, `frp_neutralizer`, `avb_patcher`), permitindo futuras extensões, como integração de GUI em PyQt5, empacotamento multiplataforma ou automatização avançada de extração de `.tar.md5`. Na minha opinião, esta abordagem modular facilita a manutenção, promove a clareza do código e confere robustez a todo o pipeline de desbloqueio.
>
> **Requisitos e ambiente:**
>
> * Windows 10/11 com WSL 2 (Ubuntu/Debian).
> * Python 3.10+, `simg2img`, `fuse`, `android-tools-fsutils`, `avbtool`, `magiskboot`.
> * Permissões de administrador/`sudo` para montagem de imagens ext4.

## Empacotamento rápido em executável Windows

Para distribuir ou utilizar a ferramenta sem abrir o terminal sempre que precisar, é possível gerar um executável `.exe` único através do PyInstaller:

1. Instale as dependências Python (incluindo o PyInstaller) numa `venv` ou ambiente global:

   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requesitos.txt
   ```

2. Execute o script auxiliar incluído no projecto:

   ```bash
   python build_windows_exe.py
   ```

3. O executável `FRP-Cleaner.exe` será criado na pasta `dist/`. Coloque-o junto dos recursos exigidos (imagens `system.img`, pasta `AP`, pasta `Keys`) e execute-o normalmente no Windows. A primeira execução demora um pouco porque o PyInstaller descomprime os ficheiros temporários.

> **Observação:** mesmo no modo executável, os utilitários externos (`simg2img`, `avbtool`, `magiskboot`, WSL com `mount`, etc.) continuam a ser necessários e devem estar configurados no sistema conforme descrito anteriormente.
>
> **Licença e responsabilidade:**
> Este software destina‑se exclusivamente a fins legítimos, em dispositivos de propriedade do utilizador ou sob autorização expressa. A utilização indevida poderá violar legislações de cibersegurança e políticas de fabricantes. Na minha opinião, a documentação rigorosa e os logs proporcionam um nível de responsabilidade e controlo imprescindível em ambientes técnicos e forenses.
>
> — Mestre Jorge Augusto Mabuie, junho de 2025


## Gerar instalador gráfico para Windows

Para distribuir o FRP Cleaner como um instalador tradicional (.exe) utilize os artefactos na pasta `instalador/`:

1. No Windows, com a `venv` activada, instale as dependências (`pip install -r requesitos.txt`).
2. Instale o [Inno Setup](https://jrsoftware.org/isinfo.php) e certifique-se de que o comando `iscc.exe` está no `PATH`.
3. Execute o script PowerShell (ele detecta automaticamente a versão definida em `cleaner.__version__` para sincronizar o executável e o instalador):
   ```powershell
   ./instalador/build_installer.ps1
   ```
4. O pacote `instalador/dist/FRP_Cleaner_Setup.exe` será gerado, copiando automaticamente o executável PyInstaller e a documentação rápida.

Caso prefira executar etapas manualmente, consulte `instalador/README.md`. O instalador final continuará a exigir o WSL e as ferramentas externas detalhadas anteriormente.
