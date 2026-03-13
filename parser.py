import json

def parse_tcp(output):
    data = json.loads(output)
    throughput_mbps = data["end"]["sum_received"]["bits_per_second"] / 1000000
    return {"throughput_mbps": throughput_mbps}

def parse_udp(output):
    data = json.loads(output)
    throughput = data["end"]["sum"]["bits_per_second"] / 1000000
    jitter_ms = data["end"]["sum"]["jitter_ms"]
    lost_pct = data["end"]["sum"]["lost_percent"]
    return {"throughput_mbps" : throughput, "jitter_ms" : jitter_ms, "lost_percent" : lost_pct}
