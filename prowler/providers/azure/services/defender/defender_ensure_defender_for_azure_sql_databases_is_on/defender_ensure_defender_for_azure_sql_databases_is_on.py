from prowler.lib.check.models import Check, Check_Report_Azure
from prowler.providers.azure.services.defender.defender_client import defender_client


class defender_ensure_defender_for_azure_sql_databases_is_on(Check):
    def execute(self) -> Check_Report_Azure:
        findings = []
        for subscription, pricings in defender_client.pricings.items():
            if "SqlServers" in pricings:
                report = Check_Report_Azure(
                    metadata=self.metadata(), resource=pricings["SqlServers"]
                )
                report.subscription = subscription
                report.status = "PASS"
                report.status_extended = f"Defender plan Defender for Azure SQL DB Servers from subscription {subscription} is set to ON (pricing tier standard)."
                if pricings["SqlServers"].pricing_tier != "Standard":
                    report.status = "FAIL"
                    report.status_extended = f"Defender plan Defender for Azure SQL DB Servers from subscription {subscription} is set to OFF (pricing tier not standard)."

                findings.append(report)
        return findings
