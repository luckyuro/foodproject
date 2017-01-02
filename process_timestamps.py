
import csv

f = open('sbux_original.csv')
csv_f = csv.reader(f)

for row in csv_f:
	if(row[0][0] == 'a'):
		timestamp = row[0][1::]
		row[0] = timestamp
	else:
		print row
		time_stamp = int(timestamp) + 300 * int(row[0])
		print time_stamp
		row[0] = time_stamp
	# write row to a new csv file. 
	with open('sbux.csv', 'ab') as f:                                    
	    writer = csv.writer(f)                                                       
	    writer.writerow(row)

