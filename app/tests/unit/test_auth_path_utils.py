import pytest

from app.config.authorization import EXCLUDE_PATHS
from app.lib import auth_path_utils as apu


def test_normalize_path_root():
    assert apu.normalize_path("/") == ""
    assert apu.normalize_path("") == ""


def test_normalize_path_strips_trailing_slash():
    assert apu.normalize_path("/health/") == "/health"
    assert apu.normalize_path("/api/v1/foo") == "/api/v1/foo"


def test_excluded_path_checker_default_config():
    check = apu.excluded_path_checker(EXCLUDE_PATHS)

    assert check("/health")
    assert check("/health/")
    assert check("/api/v1/users/login")
    assert check("/docs")
    assert check("/openapi.json")


def test_excluded_path_checker_root():
    check = apu.excluded_path_checker(EXCLUDE_PATHS)
    assert check("/")


def test_excluded_path_checker_unknown_requires_auth():
    check = apu.excluded_path_checker(EXCLUDE_PATHS)
    assert not check("/api/v1/secret")


def test_prefix_pattern():
    check = apu.excluded_path_checker([*EXCLUDE_PATHS, "/api/v1/news/*"])

    assert check("/api/v1/news")
    assert check("/api/v1/news/")
    assert check("/api/v1/news/latest")
    assert not check("/api/v1/newsletter")


def test_segment_wildcard_pattern():
    check = apu.excluded_path_checker([*EXCLUDE_PATHS, "/api/v1/product/*/delete"])

    assert check("/api/v1/product/42/delete")
    assert not check("/api/v1/product/42/edit")
    assert not check("/api/v1/product/a/b/delete")


def test_invalid_prefix_only_star_raises():
    with pytest.raises(ValueError, match="Invalid exclusion"):
        apu.excluded_path_checker(["/*"])
