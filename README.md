# CyberPulse — Real-Time Cloud SIEM & Threat Intelligence Lakehouse

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Kafka](https://img.shields.io/badge/Apache_Kafka-VPC_Streaming-231F20?style=for-the-badge&logo=apachekafka&logoColor=white)](https://kafka.apache.org/)
[![Spark](https://img.shields.io/badge/Apache_Spark-Threat_Profiling-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white)](https://spark.apache.org/)
[![dbt](https://img.shields.io/badge/dbt-Incident_Marts-FF694B?style=for-the-badge&logo=dbt&logoColor=white)](https://www.getdbt.com/)
[![Kestra](https://img.shields.io/badge/Kestra-Orchestration-8B5CF6?style=for-the-badge)](https://kestra.io/)
[![CI](https://github.com/Ghaberitsohaib/cyberpulse-data-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/Ghaberitsohaib/cyberpulse-data-platform/actions/workflows/ci.yml)

> **CyberPulse** is an enterprise-grade Security Information and Event Management (SIEM) Data Platform designed for cloud-native infrastructure defense. It ingests high-frequency VPC flow logs, Kubernetes network packet traces, and authentication attempts via Apache Kafka, runs sliding-window **Complex Event Processing (CEP)** against the **MITRE ATT&CK** matrix, lands partitioned forensic logs in a multi-tier Parquet lakehouse, and drives automated attacker profiling using Apache Spark and dbt.

---

## Architecture Diagram

```mermaid
flowchart LR
    subgraph S1["1. Threat Intelligence & Catalog Ingestion"]
        MITRE["MITRE ATT&CK Matrix"]
        Assets["Cloud Protected Asset Inventory"]
        DLT["dltHub Sync Engine"]
        MITRE --> DLT
        Assets --> DLT
    end

    subgraph S2["2. Real-Time Streaming & CEP Threat Engine"]
        VPC["AWS VPC Flow & K8s Packet Traces"]
        Kafka{{"Apache Kafka
(KRaft Mode)"}}
        CEP["Complex Event Processing (CEP)
(Brute-Force & Exfiltration Radar)"]
        LakeSink["Bronze Lakehouse Sink
(Partitioned Parquet)"]
        VPC --> Kafka
        Kafka --> CEP
        Kafka --> LakeSink
    end

    subgraph S3["3. Multi-Tier Lakehouse Storage"]
        Bronze[("Bronze Layer
(Raw Partitioned Parquet)")]
        Silver[("Silver Layer
(Typed Flow Logs)")]
        Gold[("Gold Layer
(Attacker IP Intel)")]
        Bronze --> Silver --> Gold
    end

    subgraph S4["4. Distributed Batch & Dimensional Modeling"]
        Spark["Apache Spark (PySpark)
(Attacker IP Profiling & Blocklists)"]
        DBT["dbt (Data Build Tool)
(Star Schema & Security Assertions)"]
        Warehouse[("Analytical Warehouse
(DuckDB / GCP BigQuery)")]
    end

    subgraph S5["5. Executive Command Console"]
        SOC["Streamlit SOC Command Console
(Threat Radar & Incident Forensics)"]
    end

    LakeSink --> Bronze
    DLT --> Warehouse
    Bronze --> Spark --> Gold
    Gold --> Warehouse
    Warehouse <--> DBT
    Warehouse --> SOC
    CEP --> SOC
```

---

## Key Cybersecurity Data Engineering Concepts Implemented

| Domain Concept | Implementation in CyberPulse |
| :--- | :--- |
| **Complex Event Processing (CEP)** | Inspects streaming network packets in sliding windows to flag SSH/RDP brute-force credential spraying, multi-port discovery sweeps, and exfiltration bursts. |
| **MITRE ATT&CK Classification** | Automatically maps raw firewall drop/allow events to standardized attack tactics (`T1110.001` Password Spraying, `T1046` Port Scan, `T1048.003` Exfiltration). |
| **Protected Asset Exposure Matrix** | Correlates destination IPs against critical production infrastructure (Kubernetes clusters, Postgres primaries, Bastion hosts). |
| **Distributed Attacker Profiling** | PySpark batch job calculating block rate ratios, attacked port diversity, and peak threat scores per external entity. |
| **Forensic Audit Data Quality** | Automated **dbt assertions** verifying positive packet counts, timestamp integrity, and IP address format validations. |
| **Infrastructure as Code (IaC)** | Modular **Terraform** provisioning GCP Cloud Storage buckets and partitioned BigQuery datasets for multi-year compliance. |

---

## Repository Structure

```
cyberpulse-data-platform/
├── docker-compose.yml              # Cluster: Kafka, MinIO, Spark, Kestra, Dashboard
├── requirements.txt                # Python libraries
├── terraform/                      # Terraform GCP BigQuery & GCS Buckets
├── ingestion/                      # dltHub pipelines for MITRE Matrix & Asset Catalog
├── streaming/                      # Kafka security producer, CEP threat detector, lakehouse sink
├── batch/                          # PySpark attacker profiling & blocklist generation
├── analytics_dbt/                  # dbt models (stg_*, fct_*) & automated tests
├── orchestration/flows/            # Kestra declarative workflow DAGs
├── data_platform/                  # Streamlit Executive SOC Command Console
├── scripts/                        # Automated pipeline execution scripts
└── tests/                          # Automated pytest suite
```

---

## Quickstart: Running in 30 Seconds

### 1. Install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Execute the entire pipeline locally:
```bash
python scripts/run_pipeline.py
```

### 3. Launch the SOC Command Console:
```bash
streamlit run data_platform/dashboard.py
```
Open **`http://localhost:8501`** to inspect the real-time threat radar, review attacker IP profiles, and drill down into packet-level forensic traces.

---

## Full Docker Multi-Container Cluster

```bash
docker compose up -d
```
- **SOC Command Console**: `http://localhost:8503`
- **Kafka Stream Monitor**: `http://localhost:9092`
- **MinIO Lakehouse Console**: `http://localhost:9001`
