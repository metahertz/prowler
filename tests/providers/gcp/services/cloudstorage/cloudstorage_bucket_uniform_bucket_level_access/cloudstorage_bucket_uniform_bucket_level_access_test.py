from unittest import mock

from tests.providers.gcp.gcp_fixtures import (
    GCP_PROJECT_ID,
    GCP_US_CENTER1_LOCATION,
    set_mocked_gcp_provider,
)


class TestCloudStorageBucketUniformBucketLevelAccess:
    def test_bucket_with_uniform_bucket_level_access_enabled(self):
        cloudstorage_client = mock.MagicMock()

        with (
            mock.patch(
                "prowler.providers.common.provider.Provider.get_global_provider",
                return_value=set_mocked_gcp_provider(),
            ),
            mock.patch(
                "prowler.providers.gcp.services.cloudstorage.cloudstorage_bucket_uniform_bucket_level_access.cloudstorage_bucket_uniform_bucket_level_access.cloudstorage_client",
                new=cloudstorage_client,
            ),
        ):
            from prowler.providers.gcp.services.cloudstorage.cloudstorage_bucket_uniform_bucket_level_access.cloudstorage_bucket_uniform_bucket_level_access import (
                cloudstorage_bucket_uniform_bucket_level_access,
            )
            from prowler.providers.gcp.services.cloudstorage.cloudstorage_service import (
                Bucket,
            )

            cloudstorage_client.project_ids = [GCP_PROJECT_ID]
            cloudstorage_client.region = GCP_US_CENTER1_LOCATION

            cloudstorage_client.buckets = [
                Bucket(
                    name="example-bucket",
                    id="example-bucket",
                    region=GCP_US_CENTER1_LOCATION,
                    uniform_bucket_level_access=True,
                    public=False,
                    project_id=GCP_PROJECT_ID,
                )
            ]

            check = cloudstorage_bucket_uniform_bucket_level_access()
            result = check.execute()

            assert len(result) == 1
            assert result[0].status == "PASS"
            assert (
                result[0].status_extended
                == f"Bucket {cloudstorage_client.buckets[0].name} has uniform Bucket Level Access enabled."
            )
            assert result[0].resource_id == "example-bucket"
            assert result[0].resource_name == "example-bucket"
            assert result[0].location == GCP_US_CENTER1_LOCATION
            assert result[0].project_id == GCP_PROJECT_ID

    def test_bucket_with_uniform_bucket_level_access_disabled(self):
        cloudstorage_client = mock.MagicMock()

        with (
            mock.patch(
                "prowler.providers.common.provider.Provider.get_global_provider",
                return_value=set_mocked_gcp_provider(),
            ),
            mock.patch(
                "prowler.providers.gcp.services.cloudstorage.cloudstorage_bucket_uniform_bucket_level_access.cloudstorage_bucket_uniform_bucket_level_access.cloudstorage_client",
                new=cloudstorage_client,
            ),
        ):
            from prowler.providers.gcp.services.cloudstorage.cloudstorage_bucket_uniform_bucket_level_access.cloudstorage_bucket_uniform_bucket_level_access import (
                cloudstorage_bucket_uniform_bucket_level_access,
            )
            from prowler.providers.gcp.services.cloudstorage.cloudstorage_service import (
                Bucket,
            )

            cloudstorage_client.project_ids = [GCP_PROJECT_ID]
            cloudstorage_client.region = GCP_US_CENTER1_LOCATION

            cloudstorage_client.buckets = [
                Bucket(
                    name="example-bucket",
                    id="example-bucket",
                    region=GCP_US_CENTER1_LOCATION,
                    uniform_bucket_level_access=False,
                    public=False,
                    project_id=GCP_PROJECT_ID,
                )
            ]

            check = cloudstorage_bucket_uniform_bucket_level_access()
            result = check.execute()

            assert len(result) == 1
            assert result[0].status == "FAIL"
            assert (
                result[0].status_extended
                == f"Bucket {cloudstorage_client.buckets[0].name} has uniform Bucket Level Access disabled."
            )
            assert result[0].resource_id == "example-bucket"
            assert result[0].resource_name == "example-bucket"
            assert result[0].location == GCP_US_CENTER1_LOCATION
            assert result[0].project_id == GCP_PROJECT_ID

    def test_no_buckets(self):
        cloudstorage_client = mock.MagicMock()

        with (
            mock.patch(
                "prowler.providers.common.provider.Provider.get_global_provider",
                return_value=set_mocked_gcp_provider(),
            ),
            mock.patch(
                "prowler.providers.gcp.services.cloudstorage.cloudstorage_bucket_uniform_bucket_level_access.cloudstorage_bucket_uniform_bucket_level_access.cloudstorage_client",
                new=cloudstorage_client,
            ),
        ):
            from prowler.providers.gcp.services.cloudstorage.cloudstorage_bucket_uniform_bucket_level_access.cloudstorage_bucket_uniform_bucket_level_access import (
                cloudstorage_bucket_uniform_bucket_level_access,
            )

            cloudstorage_client.project_ids = [GCP_PROJECT_ID]
            cloudstorage_client.region = GCP_US_CENTER1_LOCATION
            cloudstorage_client.buckets = []

            check = cloudstorage_bucket_uniform_bucket_level_access()
            result = check.execute()

            assert len(result) == 0
