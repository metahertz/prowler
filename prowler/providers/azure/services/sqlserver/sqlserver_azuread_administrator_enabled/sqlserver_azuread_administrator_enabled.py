from prowler.lib.check.models import Check, Check_Report_Azure
from prowler.providers.azure.services.sqlserver.sqlserver_client import sqlserver_client


class sqlserver_azuread_administrator_enabled(Check):
    def execute(self) -> Check_Report_Azure:
        findings = []
        for subscription, sql_servers in sqlserver_client.sql_servers.items():
            for sql_server in sql_servers:
                report = Check_Report_Azure(
                    metadata=self.metadata(), resource_metadata=sql_server
                )
                report.subscription = subscription
                report.status = "PASS"
                report.status_extended = f"SQL Server {sql_server.name} from subscription {subscription} has an Active Directory administrator."

                if (
                    sql_server.administrators is None
                    or sql_server.administrators.administrator_type != "ActiveDirectory"
                ):
                    report.status = "FAIL"
                    report.status_extended = f"SQL Server {sql_server.name} from subscription {subscription} does not have an Active Directory administrator."

                findings.append(report)

        return findings
