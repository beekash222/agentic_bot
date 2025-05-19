# servicenow/incident_api.py

import requests
from requests.auth import HTTPBasicAuth
from config import SERVICENOW_INSTANCE, SERVICENOW_USERNAME, SERVICENOW_PASSWORD


class ServiceNowClient:
    def __init__(self):
        self.base_url = f"{SERVICENOW_INSTANCE}/api/now/table/incident"
        self.auth = HTTPBasicAuth(SERVICENOW_USERNAME, SERVICENOW_PASSWORD)
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def create_incident(self, short_description, urgency="2", impact="2", category="inquiry"):
        payload = {
            "short_description": short_description,
            "urgency": urgency,
            "impact": impact,
            "category": category
        }

        response = requests.post(
            self.base_url,
            auth=self.auth,
            headers=self.headers,
            json=payload
        )

        if response.status_code == 201:
            result = response.json()["result"]
            return {"success": True, "incident_number": result["number"], "sys_id": result["sys_id"]}
        else:
            return {"success": False, "error": response.text}

    def update_incident(self, number, update_fields: dict):
        sys_id = self._get_sys_id_by_number(number)
        if not sys_id:
            return {"success": False, "error": f"Incident {number} not found"}

        url = f"{self.base_url}/{sys_id}"
        response = requests.patch(
            url,
            auth=self.auth,
            headers=self.headers,
            json=update_fields
        )

        if response.status_code in [200, 204]:
            return {"success": True}
        else:
            return {"success": False, "error": response.text}

    def delete_incident(self, number):
        sys_id = self._get_sys_id_by_number(number)
        if not sys_id:
            return {"success": False, "error": f"Incident {number} not found"}

        url = f"{self.base_url}/{sys_id}"
        response = requests.delete(
            url,
            auth=self.auth,
            headers=self.headers
        )

        if response.status_code in [200, 204]:
            return {"success": True}
        else:
            return {"success": False, "error": response.text}

    def _get_sys_id_by_number(self, number):
        """Helper to resolve sys_id from incident number."""
        query_url = f"{self.base_url}?sysparm_query=number={number}&sysparm_fields=sys_id"
        response = requests.get(query_url, auth=self.auth, headers=self.headers)
        if response.status_code == 200:
            results = response.json().get("result", [])
            return results[0]["sys_id"] if results else None
        return None
