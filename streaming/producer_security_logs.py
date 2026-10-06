"""
Kafka Security Log & VPC Flow Stream Producer
Emits high-velocity network packet traces, firewall logs, and authentication attempts.
"""
import uuid
import random
import time
from datetime import datetime, timezone

COUNTRIES = ["US", "DE", "FR", "GB", "NL", "RU", "CN", "IR", "KP", "BR", "IN", "MA"]
HIGH_RISK_COUNTRIES = {"RU", "CN", "IR", "KP"}

INTERNAL_IPS = [
    "10.0.1.15", "10.0.2.40", "10.0.0.5", "10.0.0.100", 
    "10.0.3.12", "10.0.3.88", "10.0.4.55"
]

EXTERNAL_ATTACKER_IPS = [
    f"185.220.{random.randint(100, 255)}.{random.randint(1, 254)}" for _ in range(12)
] + [
    f"45.154.{random.randint(10, 99)}.{random.randint(1, 254)}" for _ in range(8)
]

COMMON_PORTS = [22, 80, 443, 3389, 5432, 6379, 8080, 27017, 9092]
PROTOCOLS = ["TCP", "TCP", "TCP", "UDP", "ICMP"]

def generate_security_event():
    is_malicious = random.random() < 0.28
    
    if is_malicious:
        src_ip = random.choice(EXTERNAL_ATTACKER_IPS)
        src_country = random.choice(["RU", "CN", "IR", "KP", "NL", "US"])
        dest_ip = random.choice(INTERNAL_IPS)
        dest_port = random.choice([22, 3389, 445, 1433, 5432, 6379, 8080])
        action = random.choice(["DENY", "DENY", "DENY", "ALLOW"])
        bytes_tx = random.randint(120, 18500000) if action == "ALLOW" else random.randint(64, 512)
        log_type = random.choice(["AUTH_LOG", "VPC_FLOW", "WAF_INGRESS"])
    else:
        src_ip = f"192.168.1.{random.randint(2, 254)}" if random.random() < 0.4 else f"198.51.100.{random.randint(1, 200)}"
        src_country = random.choice(["US", "FR", "DE", "GB", "MA", "NL"])
        dest_ip = random.choice(INTERNAL_IPS)
        dest_port = random.choice([80, 443, 8080])
        action = "ALLOW"
        bytes_tx = random.randint(1200, 48000)
        log_type = "VPC_FLOW"

    now = datetime.now(timezone.utc)
    
    return {
        "event_id": f"SEC_{uuid.uuid4().hex[:12].upper()}",
        "timestamp": now.isoformat(),
        "source_ip": src_ip,
        "source_country": src_country,
        "destination_ip": dest_ip,
        "destination_port": dest_port,
        "protocol": random.choice(PROTOCOLS),
        "action": action,
        "bytes_transferred": bytes_tx,
        "packets": max(1, int(bytes_tx / 512)),
        "log_source": log_type
    }

def produce_security_stream(count=80):
    return [generate_security_event() for _ in range(count)]

if __name__ == "__main__":
    sample = produce_security_stream(5)
    print("Generated sample security event:", sample[0])
