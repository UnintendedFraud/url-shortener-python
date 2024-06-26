import pytest

from app.main import app
from app.api.api import Api

from sqlalchemy.exc import DBAPIError

from psycopg2.errors import UniqueViolation

from fastapi import HTTPException
from fastapi.testclient import TestClient


client = TestClient(app)


def iso_datetime(dt):
    return dt.isoformat()


def get_valid_short_url(mock):
    mock.created_at.isoformat.return_value = "2024-05-26T00:00:00"
    mock.last_redirect_at.isoformat.return_value = "2024-05-27T00:00:00"
    mock.redirect_count = 5
    mock.url = "https://example.com"
    mock.shortcode = "valid_"

    return mock


def get_valid_shorten_payload():
    return {
        "shortcode": "  valid_  ",
        "url": "   https://example.com  ",
    }


@pytest.fixture
def mock_session(mocker):
    return mocker.patch("app.api.endpoints.Session")


@pytest.fixture
def mock_get_by_shortcode(mocker):
    return mocker.patch("app.api.api.ShortUrlObj.get_by_shortcode")


@pytest.fixture
def mock_is_shortcode_valid(mocker):
    return mocker.patch("app.api.api.is_shortcode_valid")


@pytest.fixture
def mock_create_short_url(mocker):
    return mocker.patch("app.api.api.ShortUrlObj.create")


class Test_GetShortcode:
    def test_invalid_shortcode(self, mock_is_shortcode_valid):
        mock_is_shortcode_valid.return_value = False

        res = client.get("/invalid_shortcode")

        assert res.status_code == 400

    def test_shortcode_not_found(
        self,
        mocker,
        mock_session,
        mock_get_by_shortcode,
        mock_is_shortcode_valid,
    ):
        mock_is_shortcode_valid.return_value = True

        mock_get_by_shortcode.return_value = None

        with pytest.raises(HTTPException) as e:
            Api().redirect_to_url(mock_session, "non_existing_code")

        assert e.value.status_code == 404

    def test_use_shortcode(
            self,
            mocker,
            mock_session,
            mock_get_by_shortcode,
            mock_is_shortcode_valid,
    ):
        mock_is_shortcode_valid.return_value = True

        valid_short_url = get_valid_short_url(mocker.Mock())
        expected_redirect_count = valid_short_url.redirect_count + 1

        mock_get_by_shortcode.return_value = valid_short_url

        res = Api().redirect_to_url(mock_session, valid_short_url.shortcode)

        assert res.status_code == 302
        assert res.headers["location"] == valid_short_url.url
        assert valid_short_url.redirect_count == expected_redirect_count


class Test_ShortcodeStats:
    def test_invalid_shortcode(self, mock_is_shortcode_valid):
        mock_is_shortcode_valid.return_value = False

        res = client.get("/invalid_shortcode/stats")

        assert res.status_code == 400

    def test_shortcode_not_found(
        self,
        mocker,
        mock_get_by_shortcode,
        mock_is_shortcode_valid,
    ):
        mock_is_shortcode_valid.return_value = True

        mock_get_by_shortcode.return_value = None

        res = client.get("/valid_/stats")

        assert res.status_code == 404

    def test_everything_is_correct(
        self,
        mock_session,
        mocker,
        mock_get_by_shortcode,
        mock_is_shortcode_valid,
    ):
        mock_is_shortcode_valid.return_value = True
        mock_session.commit.return_value = None

        valid_short_url = get_valid_short_url(mocker.Mock())
        mock_get_by_shortcode.return_value = valid_short_url

        res = client.get("/valid_/stats")

        assert res.status_code == 200
        assert res.json() == {
            "created": valid_short_url.created_at.isoformat(),
            "lastRedirect": valid_short_url.last_redirect_at.isoformat(),
            "redirectCount": valid_short_url.redirect_count,
        }


class Test_Shorten:
    def test_missing_url_payload(self):
        res = client.post("/shorten", json={"shortcode": "valid_"})

        assert res.status_code == 400

    def test_invalid_url_payload(self):
        res = client.post("/shorten", json={"url": "invalid_url"})

        assert res.status_code == 400

    def test_invalid_shortcode_payload(self, mock_is_shortcode_valid):
        mock_is_shortcode_valid.return_value = False

        res = client.post("/shorten", json={
            "url": "https://example.com",
            "shortcode": "invalid_code",
        })

        assert res.status_code == 412

    def test_shortcode_already_in_use(
        self,
        mocker,
        mock_create_short_url,
        mock_is_shortcode_valid,
    ):
        mock_is_shortcode_valid.return_value = True

        mock_create_short_url.side_effect = DBAPIError(
            statement="",
            params="",
            orig=UniqueViolation(),
        )

        res = client.post("/shorten", json=get_valid_shorten_payload())

        assert res.status_code == 409

    def test_short_url_added(
        self,
        mocker,
        mock_create_short_url,
        mock_is_shortcode_valid,
    ):
        mock_is_shortcode_valid.return_value = True

        mock_create_short_url.return_value = None

        payload = get_valid_shorten_payload()

        res = client.post("/shorten", json=payload)

        assert res.status_code == 201
        assert res.json() == {"shortcode": payload["shortcode"].strip()}
