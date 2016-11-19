#coding=utf-8

if __name__ == '__main__':
    import csv
    file = 'shunicom.csv'
    data= {}
    response = {'LastEvaluatedKey': None}
    root = '1868'
    with open(file, "a+", newline="", encoding='utf-8') as datacsv:
        csvwriter = csv.writer(datacsv,dialect = ("excel"))
        for i in range(440, 449+1):
            num = root + str(i)
            csvwriter.writerow([num])
            
    print("success")