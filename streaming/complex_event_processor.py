"""
Real-Time Complex Event Processing (CEP) Security Threat Detector
Detects:
  - Brute Force Password Spraying (SSH/RDP failed auth bursts)
  - Distributed Port Scanning (rapid probes across multiple ports)
  - Data Exfiltration Spikes (>5MB outbound bursts)
  - Geographic Sanction Traffic
"""
import pandas as pd
from datetime import datetime, timezone

def evaluate_threat_signatures(events):
    df = pd.DataFrame(events)
    if df.empty:
        return events, []
    
    threat_alerts = []
    
    # 1. Group by source IP to detect velocity & multi-port attacks
    ip_stats = df.groupby("source_ip").agg(
        event_count=('event_id', 'count'),
        distinct_ports=('destination_port', 'nunique'),
        deny_count=('action', lambda s: (s == "DENY").sum()),
        total_bytes=('bytes_transferred', 'sum')
    ).to_dict(orient='index')

    scored_events = []
    now = datetime.now(timezone.utc).isoformat()
    
    for evt in events:
        ip = evt["source_ip"]
        stats = ip_stats.get(ip, {"event_count": 1, "distinct_ports": 1, "deny_count": 0, "total_bytes": 0})
        
        reasons = []
        threat_score = 10
        mitre_id = "BENIGN"
        
        # Check Brute Force (Port 22/3389 and high Deny rate)
        if evt["destination_port"] in [22, 3389] and stats["deny_count"] >= 3:
            reasons.append("BRUTE_FORCE_CREDENTIAL_SPRAYING")
            threat_score = max(threat_score, 88)
            mitre_id = "T1110.001"
            
        # Check Port Scan
        if stats["distinct_ports"] >= 4:
            reasons.append("NETWORK_PORT_SWEEP_DISCOVERY")
            threat_score = max(threat_score, 75)
            mitre_id = "T1046"

        # Check Exfiltration
        if evt["action"] == "ALLOW" and evt["bytes_transferred"] > 4000000:
            reasons.append("LARGE_VOLUME_DATA_EXFILTRATION")
            threat_score = max(threat_score, 92)
            mitre_id = "T1048.003"

        # Geographic Sanctions
        if evt["source_country"] in ["RU", "CN", "IR", "KP"]:
            reasons.append("SANCTIONED_GEOGRAPHY_INBOUND")
            threat_score = max(threat_score, 65)

        is_threat = len(reasons) > 0
        severity = "CRITICAL" if threat_score >= 85 else ("HIGH" if threat_score >= 70 else ("MEDIUM" if is_threat else "LOW"))

        evt["threat_score"] = threat_score
        evt["is_threat"] = is_threat
        evt["severity"] = severity
        evt["threat_reasons"] = "; ".join(reasons) if reasons else "BENIGN_NETWORK_FLOW"
        evt["mitre_technique_id"] = mitre_id
        scored_events.append(evt)
        
        if is_threat:
            threat_alerts.append({
                "alert_id": f"ALT_{evt['event_id'][4:]}",
                "event_id": evt["event_id"],
                "timestamp": evt["timestamp"],
                "source_ip": evt["source_ip"],
                "source_country": evt["source_country"],
                "destination_ip": evt["destination_ip"],
                "destination_port": evt["destination_port"],
                "threat_score": threat_score,
                "severity": severity,
                "mitre_technique_id": mitre_id,
                "threat_reasons": evt["threat_reasons"]
            })

    return scored_events, threat_alerts
