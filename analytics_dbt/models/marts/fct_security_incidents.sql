
SELECT 
    e.event_id,
    e.event_timestamp,
    e.source_ip,
    e.source_country,
    e.destination_ip,
    coalesce(a.asset_name, 'External Service') as targeted_asset_name,
    coalesce(a.criticality, 'STANDARD') as asset_criticality,
    e.destination_port,
    e.protocol,
    e.action,
    e.bytes_transferred,
    e.packets,
    e.threat_score,
    e.is_threat,
    e.severity,
    e.mitre_technique_id,
    e.threat_reasons
FROM cyberpulse_analytics.stg_security_events e
LEFT JOIN cyberpulse_analytics.stg_cloud_assets a ON e.destination_ip = a.ip_address;
