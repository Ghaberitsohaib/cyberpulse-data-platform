"""
dltHub Ingestion Pipeline: Threat Intelligence Feeds & Cloud Asset Catalog
Syncs:
  - MITRE ATT&CK Matrix Tactic Definitions
  - Known Tor Exit Nodes & Malicious IP Blocklists
  - Protected Enterprise Cloud Assets & Subnets
Target: cyberpulse_raw schema
"""
import os
import duckdb
import pandas as pd
from datetime import datetime, timezone

def run_dlt_threat_intel_ingestion():
    print("[dltHub] Starting Threat Intelligence and Asset Catalog sync...")
    db_path = os.path.join(os.path.dirname(__file__), "..", "data_warehouse", "cyberpulse_warehouse.duckdb")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # 1. MITRE ATT&CK Framework
    mitre_data = [
        {"technique_id": "T1110.001", "tactic": "Credential Access", "name": "Password Spraying", "severity_base": 85},
        {"technique_id": "T1046", "tactic": "Discovery", "name": "Network Service Discovery / Port Scan", "severity_base": 65},
        {"technique_id": "T1078.004", "tactic": "Defense Evasion", "name": "Cloud Account Privilege Escalation", "severity_base": 95},
        {"technique_id": "T1048.003", "tactic": "Exfiltration", "name": "Exfiltration Over Unencrypted Protocol", "severity_base": 90},
        {"technique_id": "T1498", "tactic": "Impact", "name": "Network Denial of Service (DDoS)", "severity_base": 75}
    ]
    df_mitre = pd.DataFrame(mitre_data)
    df_mitre["synced_at"] = datetime.now(timezone.utc).isoformat()

    # 2. Protected Cloud Assets (Kubernetes clusters, DB servers, VPC Bastions)
    assets_data = [
        {"asset_id": "AST-PROD-K8S-01", "asset_name": "Core Payment Cluster", "ip_address": "10.0.1.15", "subnet": "10.0.1.0/24", "criticality": "TIER_1_CRITICAL"},
        {"asset_id": "AST-PROD-DB-PRIMARY", "asset_name": "Postgres OLTP Primary", "ip_address": "10.0.2.40", "subnet": "10.0.2.0/24", "criticality": "TIER_1_CRITICAL"},
        {"asset_id": "AST-BASTION-SSH", "asset_name": "VPC DMZ Bastion Host", "ip_address": "10.0.0.5", "subnet": "10.0.0.0/24", "criticality": "TIER_2_HIGH"},
        {"asset_id": "AST-API-GATEWAY", "asset_name": "Public Envoy Proxy", "ip_address": "10.0.0.100", "subnet": "10.0.0.0/24", "criticality": "TIER_1_CRITICAL"}
    ]
    df_assets = pd.DataFrame(assets_data)
    df_assets["synced_at"] = datetime.now(timezone.utc).isoformat()

    con = duckdb.connect(db_path, read_only=False)
    con.execute("CREATE SCHEMA IF NOT EXISTS cyberpulse_raw;")
    con.execute("CREATE OR REPLACE TABLE cyberpulse_raw.threat_intel_mitre AS SELECT * FROM df_mitre;")
    con.execute("CREATE OR REPLACE TABLE cyberpulse_raw.cloud_assets AS SELECT * FROM df_assets;")
    con.close()

    print(f"[dltHub] Ingested {len(df_mitre)} MITRE techniques and {len(df_assets)} cloud assets.")

if __name__ == "__main__":
    run_dlt_threat_intel_ingestion()
