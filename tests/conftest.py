# from src.db import get_session
# from src.main import app
# from unittest.mock import AsyncMock, Mock
# import pytest
# from fastapi.testclient import TestClient
#
# mock_session_object = AsyncMock()
#
#
# def get_mock_session():
#     yield mock_session_object
#
#
# app.dependency_overrides[get_session] = get_mock_session
#
#
# @pytest.fixture
# def mock_session():
#     return mock_session_object
#
#
# @pytest.fixture
# def test_client():
#     return TestClient(app=app)
