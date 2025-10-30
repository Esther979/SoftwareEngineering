from functools import wraps

class Role:
    HR = "HR"
    FM = "FinancialManager"
    PM = "ProductionManager"  # create requests (PM = SM)

# access functions
PERMISSIONS = {
    Role.HR: {
        "approve_hr_request",
        "reject_hr_request",
        "assign_staff"
    },
    Role.FM: {
        "approve_budget",
        "reject_budget",
        "counter_offer"
    },
    Role.PM: {
        "create_hr_request",
        "create_budget_request"
    },
}

def require_permission(action_name):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            role = getattr(self, "role", None)
            if role is None:
                raise PermissionError("No role assigned")

            if action_name not in PERMISSIONS.get(role, {}):
                raise PermissionError(
                    f"Role '{role}' is not allowed to perform '{action_name}'"
                )

            print(f"[Auth ✅] {role} -> {action_name}")
            return func(self, *args, **kwargs)
        return wrapper
    return decorator
