from prowler.lib.check.models import Check, Check_Report_Azure
from prowler.providers.azure.services.app.app_client import app_client
from prowler.providers.azure.services.appinsights.appinsights_client import (
    appinsights_client,
)


class app_function_application_insights_enabled(Check):
    def execute(self):
        findings = []

        for (
            subscription_name,
            functions,
        ) in app_client.functions.items():
            for function in functions.values():
                report = Check_Report_Azure(
                    metadata=self.metadata(), resource_metadata=function
                )
                report.subscription = subscription_name
                report.status = "FAIL"
                report.status_extended = (
                    f"Function {function.name} is not using Application Insights."
                )

                if function.enviroment_variables.get(
                    "APPINSIGHTS_INSTRUMENTATIONKEY", ""
                ) in [
                    component.instrumentation_key
                    for component in appinsights_client.components[
                        subscription_name
                    ].values()
                ]:
                    report.status = "PASS"
                    report.status_extended = (
                        f"Function {function.name} is using Application Insights."
                    )

                findings.append(report)

        return findings
