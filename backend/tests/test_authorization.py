
from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from app.api.dependencies import get_current_admin


def test_regular_user_denied_admin_access():
    user = SimpleNamespace(role="user")

    with pytest.raises(HTTPException) as error:
        get_current_admin(user)

    assert error.value.status_code == 403


def test_admin_allowed_access():
    admin = SimpleNamespace(role="admin")

    result = get_current_admin(admin)

    assert result.role == "admin"
