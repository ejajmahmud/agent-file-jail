"""Filesystem sandbox preventing path traversal and symlink escapes."""
import os
from typing import Tuple, List, Set


class FileJail:
    def __init__(self, root_dir: str, blocked_extensions: List[str] = None):
        self.root_dir = os.path.abspath(root_dir)
        self.blocked_extensions: Set[str] = set(ext.lower() for ext in (blocked_extensions or [".key", ".pem", ".env"]))

    def resolve_safe_path(self, user_path: str) -> Tuple[bool, str]:
        # Collapse relative dots
        joined = os.path.normpath(os.path.join(self.root_dir, user_path.lstrip("/").lstrip("\\")))
        abs_target = os.path.abspath(joined)

        # Check if root directory is ancestor
        if not abs_target.startswith(self.root_dir):
            return False, f"Access denied: path '{user_path}' escapes sandbox root '{self.root_dir}'"

        # Check symlink escapes
        if os.path.islink(abs_target):
            real_target = os.path.realpath(abs_target)
            if not real_target.startswith(self.root_dir):
                return False, f"Access denied: symlink '{user_path}' points outside sandbox to '{real_target}'"

        # Check forbidden extensions
        _, ext = os.path.splitext(abs_target)
        if ext.lower() in self.blocked_extensions:
            return False, f"Access denied: file extension '{ext}' is forbidden in sandbox"

        return True, abs_target
