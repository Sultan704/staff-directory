"""
Automated tests for the Staff Directory API.

Run with:  pytest test_app.py -v
"""
import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client



def test_get_all_staff_returns_200(client):
    response = client.get("/staff")
    assert response.status_code == 200


def test_get_all_staff_returns_all_ten(client):
    response = client.get("/staff")
    data = response.get_json()
    assert len(data) == 10


def test_get_all_staff_returns_expected_fields(client):
    response = client.get("/staff")
    data = response.get_json()
    first = data[0]
    assert set(["id", "job_title", "research_area", "area_code", "email"]).issubset(first.keys())


# ---- /staff?area= ----

def test_filter_by_area_code_matches_brief_example(client):
    # This is the exact example given in the assignment brief: ?area=AI
    response = client.get("/staff?area=AI")
    data = response.get_json()
    assert response.status_code == 200
    assert len(data) == 2
    assert all(s["area_code"] == "AI" for s in data)


def test_filter_by_partial_area_name(client):
    response = client.get("/staff?area=cyber")
    data = response.get_json()
    assert response.status_code == 200
    assert len(data) == 2
    assert all("Cyber" in s["research_area"] for s in data)


def test_filter_is_case_insensitive(client):
    response = client.get("/staff?area=CYBER")
    data = response.get_json()
    assert len(data) == 2


def test_filter_with_no_matches_returns_empty_list(client):
    response = client.get("/staff?area=zzz_nonexistent")
    data = response.get_json()
    assert response.status_code == 200
    assert data == []


def test_filter_with_empty_string_returns_400(client):
    response = client.get("/staff?area=")
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_filter_with_overly_long_string_returns_400(client):
    response = client.get("/staff?area=" + "a" * 100)
    assert response.status_code == 400




def test_get_staff_by_valid_id(client):
    response = client.get("/staff/1")
    data = response.get_json()
    assert response.status_code == 200
    assert data["id"] == 1


def test_get_staff_by_invalid_id_returns_404(client):
    response = client.get("/staff/999")
    data = response.get_json()
    assert response.status_code == 404
    assert "error" in data


def test_get_staff_by_non_integer_id_returns_404(client):
  
    response = client.get("/staff/not-a-number")
    assert response.status_code == 404




def test_home_route_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200


def test_unknown_route_returns_json_404(client):
    response = client.get("/this-route-does-not-exist")
    data = response.get_json()
    assert response.status_code == 404
    assert "error" in data