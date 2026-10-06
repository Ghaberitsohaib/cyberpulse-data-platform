import sys, os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import duckdb
import pytest

def test_pipeline_execution():
    from scripts.run_pipeline import run_entire_pipeline
    run_entire_pipeline()

    db_path = os.path.join(ROOT_DIR, "data_warehouse", "cyberpulse_warehouse.duckdb")
    assert os.path.exists(db_path), "Warehouse database does not exist!"

    con = duckdb.connect(db_path, read_only=False)
    
    # 1. Verify security incidents
    inc_count = con.execute("SELECT count(*) FROM cyberpulse_analytics.fct_security_incidents").fetchone()[0]
    assert inc_count > 0, "No incidents in fact table!"

    # 2. Verify threat attacker profiling
    att_count = con.execute("SELECT count(*) FROM cyberpulse_analytics.spark_attacker_intel").fetchone()[0]
    assert att_count > 0, "No attacker intelligence computed!"

    # 3. Verify asset exposure
    exp_count = con.execute("SELECT count(*) FROM cyberpulse_analytics.fct_asset_exposure").fetchone()[0]
    assert exp_count > 0, "No asset exposure records computed!"

    # 4. Verify data quality
    invalid_packets = con.execute("SELECT count(*) FROM cyberpulse_analytics.fct_security_incidents WHERE packets <= 0").fetchone()[0]
    assert invalid_packets == 0, "Found invalid negative packet counts!"

    con.close()
    print("All CyberPulse pytest assertions passed successfully!")

if __name__ == "__main__":
    test_pipeline_execution()
