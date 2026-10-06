
SELECT 
    a.asset_id,
    a.asset_name,
    a.ip_address,
    a.criticality,
    count(e.event_id) as total_inbound_connections,
    sum(CASE WHEN e.action = 'DENY' THEN 1 ELSE 0 END) as blocked_connections,
    sum(CASE WHEN e.is_threat THEN 1 ELSE 0 END) as security_incidents_flagged,
    max(e.threat_score) as max_threat_score_seen
FROM cyberpulse_analytics.stg_cloud_assets a
LEFT JOIN cyberpulse_analytics.stg_security_events e ON a.ip_address = e.destination_ip
GROUP BY a.asset_id, a.asset_name, a.ip_address, a.criticality;
