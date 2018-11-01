import current_crawler as c
import datetime
from datetime import timedelta


#last 3 hours 
start_date1 = datetime.datetime.now().strftime("%Y-%m-%d")
end_date1 = datetime.datetime.now() - datetime.timedelta(hours = 3)
csvFile1 = 'train.csv'
c.collect(csvFile1,start_date1,end_date1)

start_date2 = datetime.datetime.now().strftime("%Y-%m-%d")
end_date2 = datetime.datetime.now() - datetime.timedelta(hours = 1)
csvFile2 = 'test.csv'
c.collect(csvFile2,start_date2,end_date2)
