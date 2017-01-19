import csv
import json

csvfile = open('file.csv', 'r')
jsonfile = open('file.json', 'w')

fieldnames = (
	"DateTime Stamp",
	"Bar OPEN Bid Quote", 
	"Bar HIGH Bid Quote",
	"Bar LOW Bid Quote",
	"Bar CLOSE Bid Quote",
	"Volume")
reader = csv.DictReader( csvfile, fieldnames)
for row in reader:
    json.dump(row, jsonfile)
    jsonfile.write('\n')