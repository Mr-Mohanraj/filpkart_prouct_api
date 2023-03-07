import csv

with open("./mobiledata.csv", 'r') as file:
    red = csv.DictReader(file)
    with open("data.py", 'w', encoding='utf-8') as file:
        for i in red:
            file.write(f"{str(i)},\n")