import csv
import os

def write_results(results, test_type, output_dir):
    filename = "udp_results.csv" if test_type.lower() == "udp" else "tcp_results.csv"
    with open(os.path.join(output_dir, filename), "a") as file:
        writer = csv.writer(file)
        row = [test_type]
        for key, value in results.items():
            if key == "throughput_mbps":
                row.append(f"{round(value, 2)} Mbps")
            elif key == "jitter_ms":
                row.append(f"{round(value, 2)} ms")
            elif key == "lost_percent":
                row.append(f"{round(value, 2)} %")
        writer.writerow(row)
