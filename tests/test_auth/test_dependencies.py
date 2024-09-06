from contextlib import nullcontext

import pytest
from fastapi import HTTPException

from app.auth import dependencies
from app.auth.schemas import TokenData


@pytest.mark.parametrize(
    "role, state, expectation",
    [
        (0, 0, pytest.raises(HTTPException)),
        (1, 0, pytest.raises(HTTPException)),
        (0, 1, pytest.raises(HTTPException)),
        (1, 1, nullcontext()),
        (2, 1, nullcontext()),
        (1, 2, nullcontext()),

    ]
)
async def test_check_permission(role, state, expectation):
    with expectation:
        token_data = TokenData(role=role, state=state, email='some@mail.com')
        permission = dependencies.check_permission(1, 1)
        assert await permission(token_data)
