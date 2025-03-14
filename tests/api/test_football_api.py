"""Tests for the football API client."""

import pytest
from api.football_api import FootballAPI

def test_football_api_initialization():
    api = FootballAPI()
    assert api is not None
    assert api.base_url == "https://v3.football.api-sports.io"
