
SELECT 
    event_id,
    cast(timestamp as TIMESTAMP) as event_timestamp,
    source_ip,
    source_country,
    destination_ip,
    cast(destination_port as INTEGER) as destination_port,
    protocol,
    action,
    cast(bytes_transferred as BIGINT) as bytes_transferred,
    cast(packets as INTEGER) as packets,
    log_source,
    cast(threat_score as INTEGER) as threat_score,
    is_threat,
    severity,
    threat_reasons,
    mitre_technique_id
FROM cyberpulse_raw.security_events;
