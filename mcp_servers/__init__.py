"""
mcp_servers — import bridge for the ``mcp-servers/`` directory.

Python packages cannot contain hyphens, so the filesystem layout uses
``mcp-servers/<name>-mcp/`` while the import path uses
``mcp_servers.<name>_mcp``.  This module installs a meta-path finder that
transparently maps underscore-separated import names to the corresponding
hyphen-separated directory inside ``mcp-servers/``.
"""

from __future__ import annotations

import importlib.abc
import importlib.util
import os
import sys
from typing import Optional, Sequence

_MCP_SERVERS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "mcp_servers")


class _HyphenBridgeFinder(importlib.abc.MetaPathFinder):
    """Meta-path finder that maps ``mcp_servers.<name>`` to ``mcp-servers/<name>``.

    The mapping converts underscores to hyphens in subpackage names::

        mcp_servers.ieee_xplore_mcp  →  mcp-servers/ieee-xplore-mcp/
    """

    def _resolve(self, fullname: str) -> Optional[str]:
        """Convert a dotted name to an absolute filesystem path beneath *mcp-servers/*.

        Returns ``None`` if the name is not under the ``mcp_servers.`` namespace.
        """
        parts = fullname.split(".")
        if parts[0] != "mcp_servers" or len(parts) < 2:
            return None
        # Convert each subpackage part: underscores → hyphens
        subpath = os.path.join(*[p.replace("_", "-") for p in parts[1:]])
        return os.path.join(_MCP_SERVERS_DIR, subpath)

    def find_spec(
        self,
        fullname: str,
        path: Optional[Sequence[str]] = None,
        target: Optional[object] = None,
    ) -> Optional[importlib.machinery.ModuleSpec]:
        fs_path = self._resolve(fullname)
        if fs_path is None:
            return None

        # Prefer a directory (sub-package) over a module
        if os.path.isdir(fs_path):
            init_path = os.path.join(fs_path, "__init__.py")
            if os.path.isfile(init_path):
                return importlib.util.spec_from_file_location(
                    fullname,
                    init_path,
                    submodule_search_locations=[fs_path],
                )
            # Namespace package (no __init__.py)
            return importlib.util.spec_from_file_location(
                fullname,
                None,
                submodule_search_locations=[fs_path],
            )

        # Single-file module
        py_path = fs_path + ".py"
        if os.path.isfile(py_path):
            return importlib.util.spec_from_file_location(fullname, py_path)

        return None


# Register once at import time
_FINDER = _HyphenBridgeFinder()
sys.meta_path.insert(0, _FINDER)
