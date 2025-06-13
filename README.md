# Samsung_frp_cleaner
Mestre Jorge Augusto Mabuie, segue abaixo a **descrição detalhada** do programa para inserir no seu repositório Git. Esta descrição destina‑se a fornecer uma visão clara do propósito, funcionalidades e arquitetura da ferramenta, de forma formal, expositiva e descritiva:

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
>
> **Licença e responsabilidade:**
> Este software destina‑se exclusivamente a fins legítimos, em dispositivos de propriedade do utilizador ou sob autorização expressa. A utilização indevida poderá violar legislações de cibersegurança e políticas de fabricantes. Na minha opinião, a documentação rigorosa e os logs proporcionam um nível de responsabilidade e controlo imprescindível em ambientes técnicos e forenses.
>
> — Mestre Jorge Augusto Mabuie, junho de 2025
