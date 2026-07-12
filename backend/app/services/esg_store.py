from typing import Dict, List


class ESGStore:
    def __init__(self) -> None:
        self.users: List[Dict[str, object]] = [
            {
                "id": 1,
                "name": "Ava Chen",
                "email": "ava@ecosphere.ai",
                "role": "admin",
                "department": "Operations",
            }
        ]
        self.carbon_logs: List[Dict[str, object]] = [
            {"id": 1, "source": "Electricity", "amount": 320.4, "unit": "kWh", "date": "2026-06-01"},
            {"id": 2, "source": "Fleet", "amount": 185.2, "unit": "L", "date": "2026-06-02"},
        ]
        self.csr_activities: List[Dict[str, object]] = [
            {"id": 1, "title": "River Cleanup", "location": "Lagos", "organizer": "People & Culture"},
            {"id": 2, "title": "Tree Plantation", "location": "Abuja", "organizer": "Operations"},
        ]
        self.policies: List[Dict[str, object]] = [
            {"id": 1, "title": "Sustainability Charter", "version": "v1.2", "status": "active"},
        ]

    def authenticate(self, email: str, password: str) -> Dict[str, object] | None:
        if password != "demo123":
            return None
        for user in self.users:
            if user["email"] == email:
                return user
        return None

    def register(self, name: str, email: str, password: str, role: str) -> Dict[str, object]:
        user = {
            "id": len(self.users) + 1,
            "name": name,
            "email": email,
            "role": role,
            "department": "General",
        }
        self.users.append(user)
        return user

    def get_dashboard_data(self) -> Dict[str, object]:
        return {
            "summary": [
                {"label": "Overall ESG Score", "value": "84/100", "delta": "+6%", "tone": "positive"},
                {"label": "Carbon Emissions", "value": "12.4 tCO₂e", "delta": "-8%", "tone": "positive"},
                {"label": "CSR Participation", "value": "78%", "delta": "+12%", "tone": "positive"},
                {"label": "Governance Status", "value": "Compliant", "delta": "On track", "tone": "neutral"},
            ],
            "kpis": [
                {"name": "Energy Efficiency", "value": 82, "target": 90},
                {"name": "Volunteer Hours", "value": 71, "target": 85},
                {"name": "Policy Acknowledgement", "value": 96, "target": 100},
            ],
            "initiatives": [
                "Install rooftop solar panels across two sites",
                "Launch a city cleanup challenge for regional teams",
                "Automate compliance reminders for policy renewals",
            ],
        }

    def get_carbon_logs(self) -> List[Dict[str, object]]:
        return self.carbon_logs

    def add_carbon_log(self, payload: Dict[str, object]) -> Dict[str, object]:
        log = {
            "id": len(self.carbon_logs) + 1,
            **payload,
        }
        self.carbon_logs.append(log)
        return log

    def list_csr_activities(self) -> List[Dict[str, object]]:
        return self.csr_activities

    def add_csr_activity(self, payload: Dict[str, object]) -> Dict[str, object]:
        activity = {"id": len(self.csr_activities) + 1, **payload}
        self.csr_activities.append(activity)
        return activity

    def list_policies(self) -> List[Dict[str, object]]:
        return self.policies

    def add_policy(self, payload: Dict[str, object]) -> Dict[str, object]:
        policy = {"id": len(self.policies) + 1, **payload}
        self.policies.append(policy)
        return policy


store = ESGStore()
