import requests
import random

from tests.auth.conftest import USERNAME, PASSWORD, API_URL


def test_delete_club_success(club_for_deletion, auth_headers):
    delete_response = requests.delete(
        f"{API_URL}/clubs/{club_for_deletion}/",
        headers=auth_headers
    )

    print(f"Status code DELETE: {delete_response.status_code}")
    assert delete_response.status_code == 204, f"Ожидался код 204 при удалении"


def test_delete_nonexistent_club(non_existent_club_id, auth_headers):
    """   Тест: Попытка удалить клуб с несуществующим ID.      """

    delete_response = requests.delete(
        f"{API_URL}/clubs/{non_existent_club_id}/",
        headers=auth_headers
    )

    print(f"Status code DELETE (несущ.): {delete_response.status_code}")
    assert delete_response.status_code == 404, f"Ожидался статус 404 для несуществующего ID"
