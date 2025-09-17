# simple csv report writer
import csv

def write_csv(path, rows, header=None):
    header = header or []
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        if header:
            writer.writerow(header)
        writer.writerows(rows)
