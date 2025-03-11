from unittest.mock import patch

from prowler.providers.microsoft365.models import Microsoft365IdentityInfo
from prowler.providers.microsoft365.services.entra.entra_service import (
    AdminConsentPolicy,
    AuthorizationPolicy,
    DefaultUserRolePermissions,
    Entra,
)
from tests.providers.microsoft365.microsoft365_fixtures import (
    DOMAIN,
    set_mocked_microsoft365_provider,
)


async def mock_entra_get_authorization_policy(_):
    return AuthorizationPolicy(
        id="id-1",
        name="Name 1",
        description="Description 1",
        default_user_role_permissions=DefaultUserRolePermissions(
            allowed_to_create_apps=True,
            allowed_to_create_security_groups=True,
            allowed_to_create_tenants=True,
            allowed_to_read_bitlocker_keys_for_owned_device=True,
            allowed_to_read_other_users=True,
        ),
    )


async def mock_entra_get_groups(_):
    group1 = {
        "id": "id-1",
        "name": "group1",
        "groupTypes": ["DynamicMembership"],
        "membershipRule": 'user.userType -eq "Guest"',
    }
    group2 = {
        "id": "id-2",
        "name": "group2",
        "groupTypes": ["Assigned"],
        "membershipRule": "",
    }
    return [group1, group2]


async def mock_entra_get_admin_consent_policy(_):
    return AdminConsentPolicy(
        admin_consent_enabled=True,
        notify_reviewers=True,
        email_reminders_to_reviewers=False,
        duration_in_days=30,
    )


class Test_Entra_Service:
    def test_get_client(self):
        admincenter_client = Entra(
            set_mocked_microsoft365_provider(
                identity=Microsoft365IdentityInfo(tenant_domain=DOMAIN)
            )
        )
        assert admincenter_client.client.__class__.__name__ == "GraphServiceClient"

    @patch(
        "prowler.providers.microsoft365.services.entra.entra_service.Entra._get_authorization_policy",
        new=mock_entra_get_authorization_policy,
    )
    def test_get_authorization_policy(self):
        entra_client = Entra(set_mocked_microsoft365_provider())
        assert entra_client.authorization_policy.id == "id-1"
        assert entra_client.authorization_policy.name == "Name 1"
        assert entra_client.authorization_policy.description == "Description 1"
        assert (
            entra_client.authorization_policy.default_user_role_permissions
            == DefaultUserRolePermissions(
                allowed_to_create_apps=True,
                allowed_to_create_security_groups=True,
                allowed_to_create_tenants=True,
                allowed_to_read_bitlocker_keys_for_owned_device=True,
                allowed_to_read_other_users=True,
            )
        )

    @patch(
        "prowler.providers.microsoft365.services.entra.entra_service.Entra._get_groups",
        new=mock_entra_get_groups,
    )
    def test_get_groups(self):
        entra_client = Entra(set_mocked_microsoft365_provider())
        assert len(entra_client.groups) == 2
        assert entra_client.groups[0]["id"] == "id-1"
        assert entra_client.groups[0]["name"] == "group1"
        assert entra_client.groups[0]["groupTypes"] == ["DynamicMembership"]
        assert entra_client.groups[0]["membershipRule"] == 'user.userType -eq "Guest"'
        assert entra_client.groups[1]["id"] == "id-2"
        assert entra_client.groups[1]["name"] == "group2"
        assert entra_client.groups[1]["groupTypes"] == ["Assigned"]
        assert entra_client.groups[1]["membershipRule"] == ""

    @patch(
        "prowler.providers.microsoft365.services.entra.entra_service.Entra._get_admin_consent_policy",
        new=mock_entra_get_admin_consent_policy,
    )
    def test_get_admin_consent_policy(self):
        entra_client = Entra(set_mocked_microsoft365_provider())
        assert entra_client.admin_consent_policy.admin_consent_enabled
        assert entra_client.admin_consent_policy.notify_reviewers
        assert entra_client.admin_consent_policy.email_reminders_to_reviewers is False
        assert entra_client.admin_consent_policy.duration_in_days == 30
