"""
dbt Transformation & Quality Test Runner targeting DuckDB.
"""
import os
import duckdb

def run_dbt_models():
    print("[dbt Engine] Compiling & executing SIEM staging and marts transformations...")
    db_path = os.path.join(os.path.dirname(__file__), "..", "data_warehouse", "cyberpulse_warehouse.duckdb")
    con = duckdb.connect(db_path, read_only=False)
    con.execute("CREATE SCHEMA IF NOT EXISTS cyberpulse_analytics;")

    # 1. Staging Views
    con.execute("""
        CREATE OR REPLACE VIEW cyberpulse_analytics.stg_security_events AS
        SELECT 
            event_id,
            cast(timestamp as TIMESTAMP) as event_timestamp,
            source_ip, source_country, destination_ip,
            cast(destination_port as INTEGER) as destination_port,
            protocol, action,
            cast(bytes_transferred as BIGINT) as bytes_transferred,
            cast(packets as INTEGER) as packets,
            log_source,
            cast(threat_score as INTEGER) as threat_score,
            is_threat, severity, threat_reasons, mitre_technique_id
        FROM cyberpulse_raw.security_events;
    """)

    con.execute("""
        CREATE OR REPLACE VIEW cyberpulse_analytics.stg_cloud_assets AS
        SELECT 
            asset_id, asset_name, ip_address, subnet, criticality
        FROM cyberpulse_raw.cloud_assets;
    """)

    con.execute("""
        CREATE OR REPLACE VIEW cyberpulse_analytics.stg_threat_alerts AS
        SELECT 
            alert_id, event_id,
            cast(timestamp as TIMESTAMP) as alert_timestamp,
            source_ip, source_country, destination_ip,
            cast(destination_port as INTEGER) as destination_port,
            cast(threat_score as INTEGER) as threat_score,
            severity, mitre_technique_id, threat_reasons
        FROM cyberpulse_raw.threat_alerts;
    """)

    # 2. Marts
    con.execute("""
        CREATE OR REPLACE TABLE cyberpulse_analytics.fct_security_incidents AS
        SELECT 
            e.event_id, e.event_timestamp, e.source_ip, e.source_country, e.destination_ip,
            coalesce(a.asset_name, 'External Gateway') as targeted_asset_name,
            coalesce(a.criticality, 'STANDARD') as asset_criticality,
            e.destination_port, e.protocol, e.action,
            e.bytes_transferred, e.packets, e.threat_score, e.is_threat,
            e.severity, e.mitre_technique_id, e.threat_reasons
        FROM cyberpulse_analytics.stg_security_events e
        LEFT JOIN cyberpulse_analytics.stg_cloud_assets a ON e.destination_ip = a.ip_address;
    """)

    con.execute("""
        CREATE OR REPLACE TABLE cyberpulse_analytics.fct_asset_exposure AS
        SELECT 
            a.asset_id, a.asset_name, a.ip_address, a.criticality,
            count(e.event_id) as total_inbound_connections,
            sum(CASE WHEN e.action = 'DENY' THEN 1 ELSE 0 END) as blocked_connections,
            sum(CASE WHEN e.is_threat THEN 1 ELSE 0 END) as security_incidents_flagged,
            coalesce(max(e.threat_score), 0) as max_threat_score_seen
        FROM cyberpulse_analytics.stg_cloud_assets a
        LEFT JOIN cyberpulse_analytics.stg_security_events e ON a.ip_address = e.destination_ip
        GROUP BY a.asset_id, a.asset_name, a.ip_address, a.criticality;
    """)

    # 3. Data Quality Assertions
    invalid_packets = con.execute("SELECT count(*) FROM cyberpulse_analytics.fct_security_incidents WHERE packets <= 0").fetchone()[0]
    assert invalid_packets == 0, f"dbt Test Failed: {invalid_packets} records with non-positive packets!"

    con.close()
    print("[dbt Engine] SIEM models compiled, incident marts populated, and quality assertions passed!")

if __name__ == "__main__":
    run_dbt_models()
