
SELECT 
    alert_id,
    event_id,
    cast(timestamp as TIMESTAMP) as alert_timestamp,
    source_ip,
    source_country,
    destination_ip,
    cast(destination_port as INTEGER) as destination_port,
    cast(threat_score as INTEGER) as threat_score,
    severity,
    mitre_technique_id,
    threat_reasons
FROM cyberpulse_raw.threat_alerts;
