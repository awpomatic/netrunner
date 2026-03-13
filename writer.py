import csv

def write_results(results, test_type):
    with open("results.csv", "a") as file:
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
