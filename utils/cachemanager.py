import csv


heb_cache = {}


def add_to_cache(word, results):
    global heb_cache
    heb_cache[word] = results


def save_hebrew(csv_file):
    global heb_cache
    with open(csv_file, 'w+', encoding='utf-8-sig', newline='') as f:
        heb_saver = csv.writer(f, delimiter=',')
        for w in heb_cache:
            heb_saver.writerow([w] + heb_cache[w])


def load_hebrew(csv_file):
    global heb_cache
    with open(csv_file, 'r', encoding='utf-8-sig', newline='') as f:
        file_rows = csv.reader(f, delimiter=',')
        for row in file_rows:
            heb_cache[row[0]] = row[1:]
