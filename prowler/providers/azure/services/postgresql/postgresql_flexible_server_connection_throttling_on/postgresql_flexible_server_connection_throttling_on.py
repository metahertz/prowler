from prowler.lib.check.models import Check, Check_Report_Azure
from prowler.providers.azure.services.postgresql.postgresql_client import (
    postgresql_client,
)


class postgresql_flexible_server_connection_throttling_on(Check):
    def execute(self) -> Check_Report_Azure:
        findings = []
        for (
            subscription,
            flexible_servers,
        ) in postgresql_client.flexible_servers.items():
            for server in flexible_servers:
                report = Check_Report_Azure(
                    metadata=self.metadata(), resource_metadata=server
                )
                report.subscription = subscription
                report.status = "FAIL"
                report.status_extended = f"Flexible Postgresql server {server.name} from subscription {subscription} has connection_throttling disabled"
                if server.connection_throttling == "ON":
                    report.status = "PASS"
                    report.status_extended = f"Flexible Postgresql server {server.name} from subscription {subscription} has connection_throttling enabled"
                findings.append(report)

        return findings
