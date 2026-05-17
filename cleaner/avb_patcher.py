import os
import subprocess
import logging
import platform

def to_cmd(cmd):
    """Prefixa com 'wsl' em Windows+WSL."""
    import platform, shutil as sh
    return (["wsl"] + cmd) if platform.system()=="Windows" and sh.which("wsl") else cmd

def check_runtime_dependencies():
    """Valida dependências para patch de AVB/boot."""
    import shutil as sh

    missing = []
    instructions = []

    if platform.system() == "Windows" and not sh.which("wsl"):
        missing.append("wsl")
        instructions.append("Instale/ative o WSL: execute `wsl --install` no PowerShell como Administrador.")

    for cmd in ["avbtool", "magiskboot"]:
        if not sh.which(cmd):
            missing.append(cmd)

    if missing:
        instructions.append(
            "Instale as ferramentas faltantes e garanta que estejam no PATH "
            "(ex.: `avbtool` do Android SDK e binário `magiskboot`)."
        )

    ok = not missing and not instructions
    return {
        "ok": ok,
        "missing": sorted(set(missing)),
        "instructions": instructions
    }

def patch_vbmeta(vbmeta_path, private_key_path):
    """Desativa AVB_HASHTREE e AVB_VERIFICATION em vbmeta.img."""
    out = vbmeta_path.replace(".img", "_patched.img")
    subprocess.run(to_cmd([
        "avbtool", "make_vbmeta_image",
        "--key", private_key_path,
        "--algorithm", "SHA256_RSA2048",
        "--flag", "2",  # AVB_HASHTREE_DISABLED
        "--flag", "3",  # AVB_VERIFICATION_DISABLED
        "--include_descriptors_from_image", vbmeta_path,
        "--output", out
    ]), check=True)
    logging.info(f"vbmeta patch: {vbmeta_path} → {out}")
    return out

def patch_bootimg(bootimg_path, magiskboot_path):
    """Aplica patch Magisk para contornar dm-verity no boot.img."""
    out = bootimg_path.replace(".img", "_patched.img")
    boot_dir = os.path.dirname(os.path.abspath(bootimg_path)) or "."
    boot_name = os.path.basename(bootimg_path)
    repacked_name = f"new-{boot_name}"
    repacked_path = os.path.join(boot_dir, repacked_name)

    # Desempacota e reempacota no diretório do boot para saída determinística.
    subprocess.run(to_cmd([magiskboot_path, "--unpack", boot_name]), check=True, cwd=boot_dir)
    subprocess.run(to_cmd([magiskboot_path, "--repack", boot_name]), check=True, cwd=boot_dir)

    if not os.path.exists(repacked_path):
        raise FileNotFoundError(
            f"Falha ao reempacotar {bootimg_path}: artefato esperado não foi criado ({repacked_path})."
        )

    os.replace(repacked_path, out)

    if not os.path.exists(out):
        raise FileNotFoundError(
            f"Falha ao preparar boot patch: arquivo de saída não existe após repack ({out})."
        )

    logging.info(f"boot.img patch: {bootimg_path} → {out}")
    return out
