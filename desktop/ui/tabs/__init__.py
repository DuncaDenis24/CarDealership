# Import tab classes to make them available at package level
# package initializer for ui.tabs
# Keep this file minimal to avoid importing tab modules at package import time
# This prevents circular import issues when modules import each other.

__all__ = []