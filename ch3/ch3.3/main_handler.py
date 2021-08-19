import xlrd
import csv
from py2neo import Graph, Node, Relationship


def export_relation_csv():
    '''
    整体表格正确性测试
    :return:
    '''
    data_list = [('subject', 'predicate', 'object')]
    data_sponsor_list = [('subject', 'predicate', 'object', 'ratio')]
    ExcelFile = xlrd.open_workbook('data/企业相关数据.xlsx')
    sheet = ExcelFile.sheet_by_index(0)
    for x in range(1, sheet.nrows):
        company_name = sheet.cell(x, 0).value
        area = sheet.cell(x, 3).value
        area_list = area.split(';')
        for name in area_list:
            data_list.append((company_name, '所属行业', name))
        location = sheet.cell(x, 4).value
        data_list.append((company_name, '所属地区', location))
        ceo = sheet.cell(x, 5).value
        data_list.append((company_name, '法人', ceo))
        sponsor = sheet.cell(x, 6).value
        if sponsor:
            raw_list = sponsor.split(';')
            for raw in raw_list:
                start_index = raw.index('[')
                end_index = raw.index(']')
                data_sponsor_list.append((company_name, '股东', raw[:start_index], raw[start_index+1:end_index]))
        member = sheet.cell(x, 7).value
        if member:
            member_list = member.split(';')
            for name in member_list:
                data_list.append((company_name, '主要人员', name))
        provider = sheet.cell(x, 8).value
        if provider:
            data_list.append((company_name, '供应商', provider))

    with open('data/relation_triple.csv', 'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(data_list)
    with open('data/relation_quadruples.csv', 'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(data_sponsor_list)


def import_company_data():
    g = Graph(host="192.168.1.100", port=7687, auth=('neo4j', 'kg'))
    tx = g.begin()
    a = Node("啦啦", name="Alice")
    tx.create(a)
    b = Node("哈哈", name="Jack")
    tx.create(b)
    ab = Relationship(a, "KNOWS", b)
    tx.create(ab)
    tx.commit()


if __name__ == '__main__':
    # export_relation_csv()
    import_company_data()
