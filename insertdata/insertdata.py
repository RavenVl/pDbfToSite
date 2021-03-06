from dbfread import DBF
import dataset
import csv
from shutil import copyfile
import os
from decimal import Decimal

FILENAME = 'gaz.dbf'
DBF_PATH = 'c:\\ks\\server'


def main_from_ostatki(filename=FILENAME):
    """
    function add to site data from report остатки по уровням
    :param filename:
    :return:
    """
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
        for record in _dbf:
            group = []

            for i in range(5, 0, -1):
                name = f'naim{i}'
                if record[name] != '':
                    group.append(record[name])
            group.append(record['naim'])
            group_txt = ' > '.join(group)
            try:
                cena_v_bazu = Decimal(record['cena_pr'])
            except TypeError:
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
    """
    function add to site data from 5 prod.dbf - товары and 7 marki.dbf - группы
    from /dbf directory
    :return:
    """

    dirname = os.path.dirname(__file__)
    prod_filename = os.path.join(dirname, 'dbf/prod.dbf')
    marki_filename = os.path.join(dirname, 'dbf/marki.dbf')
    result_filename = os.path.join(dirname, '../1.csv')

    copyfile(DBF_PATH + '\\prod.dbf', prod_filename)
    copyfile(DBF_PATH + '\\marki.dbf', marki_filename)

    db = dataset.connect('sqlite:///:memory:')
    table_marki = db['marki']

    for record in DBF(marki_filename, lowernames=True):
        table_marki.insert(record)

    with open(result_filename, mode="w", encoding='utf-8', newline='') as w_file:
        file_writer = csv.writer(w_file, delimiter=",")
        # file_writer = csv.writer(w_file, delimiter=",", escapechar=' ', quoting=csv.QUOTE_NONE)
        for record in DBF(prod_filename, lowernames=True):

            group = group_name_from_marki(str(record['kodm']), table_marki)
            if group is None or group.strip() == '':
                print(f'{record["kodpr"]} - нет группы')
                continue
            try:
                cena_v_bazu = Decimal(record['cena_pr'])
            except:
                print(f'{record["kodpr"]} - нет цены')
                cena_v_bazu = 0.0
            if cena_v_bazu <= 0:
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
    if cur_marka is None:
        print(f'Нет группы  - {kodm}')
        return None

    arr_kodur = cur_marka['kodur'].split()
    if len(arr_kodur) == 1:
        rez = cur_marka['naim']
    else:
        rez = ''
        arr_kodur = arr_kodur[:-1]
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
    pass
