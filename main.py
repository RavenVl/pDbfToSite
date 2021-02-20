from dbfread import DBF
import dataset
import csv


def main_from_ostatki(filename):
    pathDBF = filename
    _dbf = DBF(pathDBF, lowernames=True)
    for record in _dbf:
        group = []

        for i in range(5, 0, -1):
            name = f'naim{i}'
            if record[name] != '':
                group.append(record[name])
        # group = group + ' > ' + record['naim']
        group.append(record['naim'])
        group_txt = ' > '.join(group)

    with open("gaz_site.csv", mode="w", encoding='utf-8', newline='') as w_file:
        file_writer = csv.writer(w_file, delimiter=",")
        # file_writer = csv.writer(w_file, delimiter=",", escapechar=' ', quoting=csv.QUOTE_NONE)
        for record in _dbf:
            group = []

            for i in range(5, 0, -1):
                name = f'naim{i}'
                if record[name] != '':
                    group.append(record[name])
            # group = group + ' > ' + record['naim']
            group.append(record['naim'])
            group_txt = ' > '.join(group)
            try:
                cena_v_bazu = float(record['cena_pr'])
            except:
                print(f'{record["kodpr"]} - нет цены')
                cena_v_bazu = 0.0
            min_party = 0
            try:
                min_party = int(record['min_party'])
            except TypeError:
                pass

            kol_v_bazu = int(record['kol']) - min_party
            kol_v_bazu = kol_v_bazu if kol_v_bazu > 0 else 0
            file_writer.writerow(
                ['Газ.об.', group_txt, record['kodpr'], record['tovar'], '', 'Gaz partner', record['kodpr'],
                 cena_v_bazu,
                 kol_v_bazu])


def main_from_prod():
    db = dataset.connect('sqlite:///:memory:')
    table_marki = db['marki']

    for record in DBF('./dbf/marki.dbf', lowernames=True):
        table_marki.insert(record)

    table_prod = db['prod']
    for record in DBF('./dbf/prod.dbf', lowernames=True):
        table_prod.insert(record)

    with open("gaz_site_2.csv", mode="w", encoding='utf-8', newline='') as w_file:
        file_writer = csv.writer(w_file, delimiter=",")
        # file_writer = csv.writer(w_file, delimiter=",", escapechar=' ', quoting=csv.QUOTE_NONE)
        for record in table_prod.all():

            group = group_name_from_marki(str(record['kodm']), table_marki)
            try:
                cena_v_bazu = float(record['cena_pr'])
            except:
                print(f'{record["kodpr"]} - нет цены')
                cena_v_bazu = 0.0
            if cena_v_bazu<= 0:
                print(f'{record["kodpr"]} - нет цены')
                continue

            kol_v_bazu = 1
            file_writer.writerow(
                ['Газ.об.', group, record['kodpr'], record['naim'], '', 'Gaz partner', record['kodpr'], cena_v_bazu,
                 kol_v_bazu])


def group_name_from_marki(kodm, table_marki=None):
    if table_marki is None:
        db = dataset.connect('sqlite:///:memory:')
        table_marki = db['marki']
        for record in DBF('./dbf/marki.dbf', lowernames=True):
            table_marki.insert(record)

    cur_marka = table_marki.find_one(kodm=kodm)
    print(cur_marka)

    if kodm == cur_marka['kodur'].strip():
        rez = cur_marka['naim']
    else:
        rez = ''
        arr_kodur = cur_marka['kodur'].split()[:-1]
        kod_v_base = ''
        for kodur in arr_kodur:
            len_space = 5 - len(kodur)
            kod_v_base += ' ' * len_space + kodur
            name_kodur = table_marki.find_one(kodur=kod_v_base)['naim']
            if rez == '':
                rez = name_kodur
            else:
                rez = f'{rez} > {name_kodur}'
            pass
        rez += f' > {cur_marka["naim"]}'

    return rez


if __name__ == '__main__':
    # filename = 'gaz.dbf'
    # main(filename)
    main_from_prod()
