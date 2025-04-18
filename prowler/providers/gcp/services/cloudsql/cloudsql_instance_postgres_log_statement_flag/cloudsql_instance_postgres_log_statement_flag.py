from prowler.lib.check.models import Check, Check_Report_GCP
from prowler.providers.gcp.services.cloudsql.cloudsql_client import cloudsql_client


class cloudsql_instance_postgres_log_statement_flag(Check):
    def execute(self) -> Check_Report_GCP:
        desired_log_statement = "ddl"
        findings = []
        for instance in cloudsql_client.instances:
            if "POSTGRES" in instance.version:
                report = Check_Report_GCP(metadata=self.metadata(), resource=instance)
                report.status = "FAIL"
                report.status_extended = f"PostgreSQL Instance {instance.name} does not have 'log_statement' flag set to '{desired_log_statement}'."
                for flag in instance.flags:
                    if (
                        flag.get("name", "") == "log_statement"
                        and flag.get("value", "none") == desired_log_statement
                    ):
                        report.status = "PASS"
                        report.status_extended = f"PostgreSQL Instance {instance.name} has 'log_statement' flag set to '{desired_log_statement}'."
                        break
                findings.append(report)

        return findings
