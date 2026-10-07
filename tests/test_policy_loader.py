from app.security.policy.policy_loader import PolicyLoader


def test_policy_loader():

    loader = PolicyLoader()

    policies = loader.load()

    assert isinstance(policies, list)
    assert len(policies) > 0


def test_policy_fields():

    loader = PolicyLoader()

    policies = loader.load()

    for policy in policies:
        assert "name" in policy
        assert "action" in policy

        assert (
            policy["action"]
            in {
                "ALLOW",
                "DENY",
                "REQUIRE_APPROVAL",
            }
        )