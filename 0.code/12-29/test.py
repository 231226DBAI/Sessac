import csv
file_name = 'card.csv'
with open('card.csv', 'r', encoding='utf-8') as f:
    data = csv.reader(f)





#print(type(data))



#next(data)  #data의 첫번째 자료를 지남 -> 
for row in data:
    print(row)
    


#title = data[0]

#aim_data = data[1:4]

#num= title.index('이용금액')

