import os
import subprocess
import logging
import hashlib
import shutil
import platform
from .avb_patcher import patch_vbmeta, patch_bootimg

MOUNT_POINT = "/mnt/frp_clean_temp"

def to_cmd(cmd):
    """Prefixa com 'wsl' em Windows+WSL."""
    import platform, shutil as sh
    return (["wsl"] + cmd) if platform.system()=="Windows" and sh.which("wsl") else cmd

def check_runtime_dependencies():
    """Valida dependências de runtime e requisitos de montagem."""
    import shutil as sh

    missing = []
    instructions = []

    if platform.system() == "Windows":
        if not sh.which("wsl"):
            missing.append("wsl")
            instructions.append("Instale/ative o WSL: execute `wsl --install` no PowerShell como Administrador.")

    for cmd in ["simg2img", "tar", "sudo", "mount", "umount"]:
        if not sh.which(cmd):
            missing.append(cmd)

    if missing:
        instructions.append(
            "No WSL/Ubuntu, instale os pacotes necessários: "
            "`sudo apt update && sudo apt install -y android-sdk-libsparse-utils tar util-linux sudo`."
        )

    # Permissões de montagem
    if platform.system() != "Windows" and os.geteuid() != 0 and not sh.which("sudo"):
        instructions.append("Montagem exige root ou sudo. Rode como root ou instale/configure sudo.")

    if sh.which("sudo"):
        probe = subprocess.run(
            to_cmd(["sudo", "-n", "true"]),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        if probe.returncode != 0:
            instructions.append("Permissão sudo necessária para mount/umount. Execute uma vez `sudo -v` e tente novamente.")

    ok = not missing and not instructions
    return {
        "ok": ok,
        "missing": sorted(set(missing)),
        "instructions": instructions
    }

def ensure_mount_point():
    os.makedirs(MOUNT_POINT, exist_ok=True)

def convert_sparse_to_raw(input_img):
    output_img = input_img.replace(".img", "_raw.img")
    subprocess.run(to_cmd(["simg2img", input_img, output_img]), check=True)
    logging.info(f"Convertido sparse→raw: {input_img}→{output_img}")
    return output_img

def mount_image(img_path):
    ensure_mount_point()
    subprocess.run(to_cmd(["sudo", "mount", "-o", "loop", img_path, MOUNT_POINT]), check=True)
    logging.info(f"Montado: {img_path} em {MOUNT_POINT}")
    return MOUNT_POINT

def unmount_image():
    subprocess.run(to_cmd(["sudo", "umount", MOUNT_POINT]), check=True)
    logging.info(f"Desmontado: {MOUNT_POINT}")

def repack_tar_with_md5(input_folder, output_tar):
    # Empacotar via tar (no WSL ou local)
    subprocess.run(to_cmd([
        "tar", "-H", "ustar", "-c", "-f", output_tar,
        "-C", input_folder, "."
    ]), check=True)

    # Calcular MD5 em Python
    hash_md5 = hashlib.md5()
    with open(output_tar, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hash_md5.update(chunk)
    md5sum = hash_md5.hexdigest()
    with open(output_tar + ".md5", "w") as fp:
        fp.write(f"{md5sum}  {os.path.basename(output_tar)}")
    logging.info(f"Reempacotado: {output_tar} (+.md5 gerado)")

def prepare_and_patch_all(ap_folder, keys_folder):
    vbmeta_path = os.path.join(ap_folder, "vbmeta.img")
    bootimg_path = os.path.join(ap_folder, "boot.img")

    # Patch vbmeta
    if os.path.exists(vbmeta_path):
        patched = patch_vbmeta(vbmeta_path, os.path.join(keys_folder, "avb_private.pem"))
        shutil.move(patched, vbmeta_path)

    # Patch boot.img
    if os.path.exists(bootimg_path):
        patched = patch_bootimg(bootimg_path, os.path.join(keys_folder, "magiskboot"))
        shutil.move(patched, bootimg_path)

    # Reempacotar
    output_tar = os.path.abspath("AP_clean.tar")
    repack_tar_with_md5(ap_folder, output_tar)
    return output_tar + ".md5"
