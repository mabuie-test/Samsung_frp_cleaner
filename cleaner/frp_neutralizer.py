import os
import shutil
import logging


def _rollback(operations):
    """Reverte operações já concluídas na ordem inversa."""
    for operation in reversed(operations):
        op_type = operation["operation"]
        origin = operation["origin"]
        destination = operation["destination"]

        try:
            if op_type == "rename":
                if os.path.exists(destination):
                    os.rename(destination, origin)
                    logging.info(
                        "Rollback aplicado | operação=rename | origem=%s | destino=%s",
                        destination,
                        origin,
                    )
            elif op_type == "remove_file":
                if os.path.exists(destination):
                    os.makedirs(os.path.dirname(origin), exist_ok=True)
                    os.rename(destination, origin)
                    logging.info(
                        "Rollback aplicado | operação=restore_file | origem=%s | destino=%s",
                        destination,
                        origin,
                    )
            elif op_type == "remove_dir":
                if os.path.exists(destination):
                    os.makedirs(os.path.dirname(origin), exist_ok=True)
                    os.rename(destination, origin)
                    logging.info(
                        "Rollback aplicado | operação=restore_dir | origem=%s | destino=%s",
                        destination,
                        origin,
                    )
        except Exception as rollback_error:
            logging.error(
                "Falha no rollback | operação=%s | origem=%s | destino=%s | erro=%s",
                op_type,
                origin,
                destination,
                rollback_error,
            )

def neutralize(target_paths, strategy="rename"):
    """
    Neutraliza alvos FRP:
     - rename: renomeia adicionando .disabled
     - remove: elimina ficheiros/pastas
    """
    operations = []
    backup_root = None

    try:
        if strategy == "remove":
            first_target = target_paths[0] if target_paths else os.getcwd()
            first_parent = os.path.dirname(first_target) or os.getcwd()
            backup_root = os.path.join(first_parent, ".frp_backup_tmp")
            os.makedirs(backup_root, exist_ok=True)

        for idx, path in enumerate(target_paths):
            if strategy == "remove":
                backup_path = os.path.join(backup_root, f"item_{idx}")
                os.rename(path, backup_path)
                op_kind = "remove_dir" if os.path.isdir(backup_path) else "remove_file"
                operations.append({
                    "operation": op_kind,
                    "origin": path,
                    "destination": backup_path,
                })
                logging.info(
                    "Alteração FRP | operação=remove | origem=%s | destino=%s",
                    path,
                    backup_path,
                )
            else:
                new_path = f"{path}.disabled"
                os.rename(path, new_path)
                operations.append({
                    "operation": "rename",
                    "origin": path,
                    "destination": new_path,
                })
                logging.info(
                    "Alteração FRP | operação=rename | origem=%s | destino=%s",
                    path,
                    new_path,
                )

        if strategy == "remove" and backup_root and os.path.exists(backup_root):
            shutil.rmtree(backup_root)

        return operations
    except Exception as error:
        logging.error("Erro ao neutralizar FRP: %s", error)
        _rollback(operations)
        raise RuntimeError(
            "Falha durante neutralização FRP; rollback automático executado."
        ) from error
