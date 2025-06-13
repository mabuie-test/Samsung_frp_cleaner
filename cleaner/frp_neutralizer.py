import os
import shutil
import logging

def neutralize(target_paths, strategy="rename"):
    """
    Neutraliza alvos FRP:
     - rename: renomeia adicionando .disabled
     - remove: elimina ficheiros/pastas
    """
    for path in target_paths:
        try:
            if strategy == "remove":
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
                logging.info(f"Removido: {path}")
            else:
                new_path = f"{path}.disabled"
                os.rename(path, new_path)
                logging.info(f"Renomeado: {path} → {new_path}")
        except Exception as e:
            logging.error(f"Erro ao neutralizar {path}: {e}")
