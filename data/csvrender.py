import csv
with open('naukri_scraped_data.csv','r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print(row[0],row[1],row[5],row[6],row[-1])