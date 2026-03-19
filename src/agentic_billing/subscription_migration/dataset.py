"""Representative dataset of migration scenarios with expected outcomes.

Each scenario pairs an input event with the action a well-calibrated model
should choose.  Used by the evaluation runner to compare actual vs expected.
"""

MIGRATION_SCENARIOS = [
    {
        "name": "Standard upgrade at renewal",
        "input": {
            "customer_id": "cust_201",
            "current_plan": "starter",
            "requested_plan": "professional",
            "is_grandfathered": False,
            "is_mid_cycle": False,
            "current_price": 29.0,
            "new_price": 99.0,
            "months_on_current_plan": 6,
        },
        "expected_action": "IMMEDIATE_PRORATED_MIGRATION",
    },
    {
        "name": "Mid-cycle upgrade, small price difference",
        "input": {
            "customer_id": "cust_202",
            "current_plan": "professional",
            "requested_plan": "professional_plus",
            "is_grandfathered": False,
            "is_mid_cycle": True,
            "current_price": 99.0,
            "new_price": 129.0,
            "months_on_current_plan": 3,
        },
        "expected_action": "SCHEDULE_MIGRATION_AT_RENEWAL",
    },
    {
        "name": "Grandfathered enterprise customer, large price increase",
        "input": {
            "customer_id": "cust_203",
            "current_plan": "enterprise_legacy",
            "requested_plan": "enterprise_v2",
            "is_grandfathered": True,
            "is_mid_cycle": True,
            "current_price": 199.0,
            "new_price": 499.0,
            "months_on_current_plan": 36,
        },
        "expected_action": "PRESERVE_GRANDFATHERED_PRICE",
    },
    {
        "name": "Loyal customer upgrading, significant price jump",
        "input": {
            "customer_id": "cust_204",
            "current_plan": "starter",
            "requested_plan": "enterprise",
            "is_grandfathered": False,
            "is_mid_cycle": False,
            "current_price": 29.0,
            "new_price": 299.0,
            "months_on_current_plan": 24,
        },
        "expected_action": "MIGRATE_WITH_COMPENSATION_DISCOUNT",
    },
    {
        "name": "Grandfathered mid-cycle with moderate price change",
        "input": {
            "customer_id": "cust_205",
            "current_plan": "business_v1",
            "requested_plan": "business_v2",
            "is_grandfathered": True,
            "is_mid_cycle": True,
            "current_price": 149.0,
            "new_price": 249.0,
            "months_on_current_plan": 18,
        },
        "expected_action": "ESCALATE_TO_HUMAN",
    },
]
