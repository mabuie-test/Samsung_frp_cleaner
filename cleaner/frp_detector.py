import os

DEFAULT_TARGETS = [
    "app/SetupWizard",
    "priv-app/SetupWizard",
    "app/GoogleLoginService",
    "priv-app/FRPHandler",
    "framework/com.android.frp.jar",
    "bin/frp_check.sh",
    "etc/init.d/99frp"
]

def detect_targets(mount_dir, custom_targets=None):
    targets = custom_targets or DEFAULT_TARGETS
    encontrados = []
    for rel in targets:
        path = os.path.join(mount_dir, rel)
        if os.path.exists(path):
            encontrados.append(path)
    return encontrados
