from dbfread import DBF
import csv


def main(filename):
    pathDBF = filename
    _dbf = DBF(pathDBF, lowernames=True)
    for record in _dbf:
        group = []

        for i in range(5, 0, -1):
            name = f'naim{i}'
            if record[name] !='':
                group.append(record[name])
        # group = group + ' > ' + record['naim']
        group.append(record['naim'])
        group_txt = ' > '.join(group)
        print(group_txt)

    with open("gaz_site.csv", mode="w", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
        for record in _dbf:
            group = []

            for i in range(5, 0, -1):
                name = f'naim{i}'
                if record[name] != '':
                    group.append(record[name])
            # group = group + ' > ' + record['naim']
            group.append(record['naim'])
            group_txt = ' > '.join(group)
            print(group_txt)
            file_writer.writerow(['Газю.об.', group_txt, record['kodpr'], record['tovar'], '','','Gaz partner', record['cena'], record['kol'] ])


if __name__ == '__main__':
    filename = 'gaz.dbf'
    main(filename)
