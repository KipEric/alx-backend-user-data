#!/usr/bin/env python3
"""
Module for authentification
"""

from flask import request
from typing import List, TypeVar
import fnmatch


class Auth:
    """
    Athentification class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Function that check if authentification is needed
        """
        if path is None or excluded_paths is None or not excluded_paths:
            return True
        for excluded_path in excluded_paths:
            if excluded_path.endswith('/'):
                excluded_path = excluded_path[:-1]
            if path == excluded_path or path.startswith(excluded_path + '/'):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Function to check authorization
        """
        if request is None or "Authorization" not in request.headers:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Function to get user
        """
        return None
