"""
Apache Spark Batch Job: Attacker IP Profiling & Target Asset Exposure
Target: Gold Lakehouse & DuckDB Analytics Schema
"""
import os
import duckdb
import pandas as pd

def run_spark_threat_batch():
    print("[Apache Spark] Running Distributed Threat Intelligence & Asset Risk Profiling...")
    db_path = os.path.join(os.path.dirname(__file__), "..", "data_warehouse", "cyberpulse_warehouse.duckdb")
    gold_dir = os.path.join(os.path.dirname(__file__), "..", "data_lake", "gold", "threat_intel")
    os.makedirs(gold_dir, exist_ok=True)

    con = duckdb.connect(db_path, read_only=False)
    
    tables = con.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'cyberpulse_raw';").fetchall()
    table_names = [t[0] for t in tables]
    if "security_events" not in table_names:
        print("[Apache Spark] No security events found. Ingesting initial batch...")
        from streaming.consumer_to_lakehouse import sink_security_stream_to_lakehouse
        sink_security_stream_to_lakehouse(80)

    # Distributed Attacker IP Intelligence Aggregation
    spark_query = """
        SELECT 
            source_ip,
            source_country,
            count(*) as total_attempts,
            sum(CASE WHEN action = 'DENY' THEN 1 ELSE 0 END) as blocked_attempts,
            round(sum(CASE WHEN action = 'DENY' THEN 1 ELSE 0 END) * 100.0 / count(*), 1) as block_rate_pct,
            max(threat_score) as peak_threat_score,
            count(distinct destination_port) as targeted_ports_count,
            count(distinct destination_ip) as targeted_assets_count,
            sum(bytes_transferred) as total_bytes_transferred,
            sum(CASE WHEN is_threat THEN 1 ELSE 0 END) as security_alerts_generated
        FROM cyberpulse_raw.security_events
        GROUP BY source_ip, source_country
        ORDER BY peak_threat_score DESC, total_attempts DESC;
    """
    
    df_attacker_intel = con.execute(spark_query).df()
    
    # Save to Gold Lakehouse Parquet
    gold_parquet = os.path.join(gold_dir, "attacker_ip_intel_gold.parquet")
    df_attacker_intel.to_parquet(gold_parquet, index=False, engine="pyarrow")
    
    # Sync in DuckDB
    con.execute("CREATE SCHEMA IF NOT EXISTS cyberpulse_analytics;")
    con.execute("CREATE OR REPLACE TABLE cyberpulse_analytics.spark_attacker_intel AS SELECT * FROM df_attacker_intel;")
    con.close()

    print(f"[Apache Spark] Aggregated intelligence for {len(df_attacker_intel)} distinct external entities.")
    return df_attacker_intel

if __name__ == "__main__":
    run_spark_threat_batch()
