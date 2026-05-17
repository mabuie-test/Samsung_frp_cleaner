import argparse
import logging
import sys
from pathlib import Path

from cleaner.img_manager import (
    convert_sparse_to_raw,
    mount_image,
    unmount_image,
    prepare_and_patch_all,
    check_runtime_dependencies as check_img_runtime_dependencies
)
from cleaner.avb_patcher import check_runtime_dependencies as check_avb_runtime_dependencies
from cleaner.frp_detector import detect_targets
from cleaner.frp_neutralizer import neutralize


def _resolve_base_dir() -> Path:
    """Return the directory where auxiliary files should be stored."""
    if getattr(sys, "frozen", False):  # PyInstaller executável
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent


BASE_DIR = _resolve_base_dir()
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Configuração do log
logging.basicConfig(
    filename=str(LOG_DIR / "frp_cleaner.log"),
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)

def process_image(img_path, strategy, ap_folder, keys_folder):
    # 1. Converter se imagem for sparse
    raw = img_path
    if "sparse" in img_path:
        raw = convert_sparse_to_raw(img_path)

    # 2. Montar, detectar e neutralizar FRP
    mount_dir = mount_image(raw)
    targets = detect_targets(mount_dir)
    if targets:
        logging.info(f"Alvos FRP detectados: {targets}")
        neutralize(targets, strategy)
    else:
        logging.info("Nenhum alvo FRP encontrado.")
    unmount_image()

    # 3. Patch AVB & boot, reempacotar em .tar.md5
    final_pkg = prepare_and_patch_all(ap_folder, keys_folder)
    print(f"[OK] Pacote final pronto: {final_pkg}")
    logging.info(f"Processo concluído. Pacote: {final_pkg}")

def validate_environment_or_raise():
    img_diag = check_img_runtime_dependencies()
    avb_diag = check_avb_runtime_dependencies()

    missing = sorted(set(img_diag["missing"] + avb_diag["missing"]))
    instructions = img_diag["instructions"] + avb_diag["instructions"]

    if missing or instructions:
        msg = ["Ambiente inválido para execução do FRP Cleaner."]
        if missing:
            msg.append("Dependências ausentes: " + ", ".join(missing))
        if instructions:
            msg.append("Correções sugeridas:")
            for item in instructions:
                msg.append(f"- {item}")
        raise RuntimeError("\n".join(msg))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="FRP Cleaner Samsung (Windows+WSL)"
    )
    parser.add_argument("img", help="Caminho para system.img ou sparse.img")
    parser.add_argument("ap_folder", help="Pasta com ROM extraída (AP, BL, CP, vbmeta etc.)")
    parser.add_argument("keys_folder", help="Pasta com avb_private.pem e magiskboot")
    parser.add_argument(
        "--strategy", choices=["rename","remove"], default="rename",
        help="Estratégia de neutralização FRP (default: rename)"
    )
    args = parser.parse_args()
    validate_environment_or_raise()
    process_image(args.img, args.strategy, args.ap_folder, args.keys_folder)
