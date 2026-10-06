"""
Kafka Security Stream Consumer to Bronze Parquet Lakehouse Sink
"""
import os
import duckdb
import pandas as pd
from datetime import datetime, timezone
from streaming.producer_security_logs import produce_security_stream
from streaming.complex_event_processor import evaluate_threat_signatures

def sink_security_stream_to_lakehouse(batch_size=80):
    lake_dir = os.path.join(os.path.dirname(__file__), "..", "data_lake", "bronze", "network_logs")
    db_path = os.path.join(os.path.dirname(__file__), "..", "data_warehouse", "cyberpulse_warehouse.duckdb")
    os.makedirs(lake_dir, exist_ok=True)
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    print(f"[Security Stream Sink] Ingesting & scoring {batch_size} security events...")
    raw_events = produce_security_stream(batch_size)
    scored_events, threat_alerts = evaluate_threat_signatures(raw_events)
    
    df_events = pd.DataFrame(scored_events)
    df_alerts = pd.DataFrame(threat_alerts) if threat_alerts else pd.DataFrame(columns=[
        "alert_id", "event_id", "timestamp", "source_ip", "source_country", 
        "destination_ip", "destination_port", "threat_score", "severity", "mitre_technique_id", "threat_reasons"
    ])

    # 1. Partitioned Lakehouse Parquet Sink
    now = datetime.now(timezone.utc)
    part_dir = os.path.join(lake_dir, f"year={now.year}", f"month={now.month:02d}", f"day={now.day:02d}")
    os.makedirs(part_dir, exist_ok=True)
    parquet_path = os.path.join(part_dir, f"sec_events_{int(now.timestamp())}.parquet")
    df_events.to_parquet(parquet_path, index=False, engine="pyarrow")

    # 2. Sync to DuckDB Raw Landing
    con = duckdb.connect(db_path, read_only=False)
    con.execute("CREATE SCHEMA IF NOT EXISTS cyberpulse_raw;")
    con.execute("CREATE OR REPLACE TABLE cyberpulse_raw.security_events AS SELECT * FROM df_events;")
    con.execute("CREATE OR REPLACE TABLE cyberpulse_raw.threat_alerts AS SELECT * FROM df_alerts;")
    con.close()

    print(f"[Lakehouse Sink] Successfully landed {len(df_events)} network logs & {len(threat_alerts)} active threat alerts!")

if __name__ == "__main__":
    sink_security_stream_to_lakehouse(60)
