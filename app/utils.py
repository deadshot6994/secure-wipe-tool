import os

def is_safe_path(path):
    """Prevent wiping critical system directories."""
    system_paths = [
        "C:\\Windows", "C:\\Program Files", "C:\\Program Files (x86)", 
        "/bin", "/etc", "/usr", "/boot"
    ]
    for sys_path in system_paths:
        if path.startswith(sys_path):
            return False
    return os.path.exists(path)
