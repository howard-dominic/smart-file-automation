import csv
import os

def generate_report(sorted_files, folder_path):
    report_file = os.path.join(folder_path, "sorting_report.csv")
    with open(report_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["File Name", "Moved To"])
        for filename, folder in sorted_files:
            writer.writerow([filename, folder])
    print(f"Report generated: {report_file}")
