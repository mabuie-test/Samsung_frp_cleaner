import os
import subprocess
import logging

def to_cmd(cmd):
    """Prefixa com 'wsl' em Windows+WSL."""
    import platform, shutil as sh
    return (["wsl"] + cmd) if platform.system()=="Windows" and sh.which("wsl") else cmd

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
    # Desempacota e reempacota
    subprocess.run(to_cmd([magiskboot_path, "--unpack", bootimg_path]), check=True)
    subprocess.run(to_cmd([magiskboot_path, "--repack", bootimg_path]), check=True)
    logging.info(f"boot.img patch: {bootimg_path} → {out}")
    return out
