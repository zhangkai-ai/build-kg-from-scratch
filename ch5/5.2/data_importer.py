#!/usr/bin/env python

import xlrd
from kg_dao import kg_dao

# 标准数据字段表
ExcelFile = xlrd.open_workbook('path/to/data')

# 构建节点字典
company_node_dict = {}
molecule_node_dict = {}
person_node_dict = {}
indication_node_dict = {}
ip_node_dict = {}
# 建立边关系，边关系建立时，出节点的优先级判定：molecule > company > person > ...
molecule_rel_dict = {
    'indication': [],
    'company': [],
    'person': [],
    'IP': []
}
company_rel_dict = {
    'IP': [],
    'person': []
}
person_rel_dict = {
    'IP': []
}


def xlsx_process_company():
    sheet = ExcelFile.sheet_by_name('Company')
    for x in range(1, sheet.nrows):
        company_id = sheet.cell(x, 0).value         # 公司id,字符型
        company_name_eng = sheet.cell(x, 1).value   # 公司英文名,字符型
        company_name_chn = sheet.cell(x, 2).value   # 公司中文名,字符型
        is_on_market = sheet.cell(x, 3).value       # 公司是否上市,布尔型
        company_size = sheet.cell(x, 4).value       # 公司规模,数值型
        company_address = sheet.cell(x, 5).value    # 公司地址,字符型

        # 更新公司节点
        if company_id not in company_node_dict:
            company_node_dict[company_id] = {}
        company_detail = company_node_dict[company_id]
        company_detail['company_id'] = company_id
        company_detail['company_name_eng'] = company_name_eng
        company_detail['company_name_chn'] = company_name_chn
        company_detail['is_on_market'] = is_on_market
        company_detail['company_size'] = company_size
        company_detail['company_address'] = company_address


def xlsx_process_molecule():
    sheet = ExcelFile.sheet_by_name('Molecule')
    for x in range(1, sheet.nrows):
        molecule_id = sheet.cell(x, 0).value        # 分子id,字符型
        molecule_name_eng = sheet.cell(x, 1).value  # 分子英文名,字符型
        sequence = sheet.cell(x, 2).value
        drug_type = sheet.cell(x, 3).value
        cell_type = sheet.cell(x, 4).value

        # 更新分子节点
        if molecule_id not in molecule_node_dict:
            molecule_node_dict[molecule_id] = {}
        molecule_detail = molecule_node_dict[molecule_id]
        molecule_detail['molecule_id'] = molecule_id
        molecule_detail['molecule_name_eng'] = molecule_name_eng
        molecule_detail['sequence'] = sequence
        molecule_detail['drug_type'] = drug_type
        molecule_detail['cell_type'] = cell_type


def xlsx_process_person():
    sheet = ExcelFile.sheet_by_name('Person')
    for x in range(1, sheet.nrows):
        person_id = sheet.cell(x, 0).value      # 人物id,字符型
        person_name = sheet.cell(x, 1).value    # 人物名,字符型
        person_age = sheet.cell(x, 2).value     # 人物年龄,字符型

        # 更新人物节点
        if person_id not in person_node_dict:
            person_node_dict[person_id] = {}
        person_detail = person_node_dict[person_id]
        person_detail['person_id'] = person_id
        person_detail['person_name'] = person_name
        person_detail['person_age'] = person_age


def xlsx_process_indication():
    sheet = ExcelFile.sheet_by_name('Indication')
    for x in range(1, sheet.nrows):
        indication_id = sheet.cell(x, 0).value      # 适应症id,字符型
        indication_name = sheet.cell(x, 1).value    # 适应症名字,字符型

        # 更新适应症节点
        if indication_id not in indication_node_dict:
            indication_node_dict[indication_id] = {}
        indication_detail = indication_node_dict[indication_id]
        indication_detail['indication_id'] = indication_id
        indication_detail['indication_name'] = indication_name


def xlsx_process_ip():
    sheet = ExcelFile.sheet_by_name('IP')
    for x in range(1, sheet.nrows):
        ip_id = sheet.cell(x, 0).value      # 专利id,字符型
        ip_name = sheet.cell(x, 1).value    # 专利名,字符型

        # 更新专利节点
        if ip_id not in ip_node_dict:
            ip_node_dict[ip_id] = {}
        ip_detail = ip_node_dict[ip_id]
        ip_detail['ip_id'] = ip_id
        ip_detail['ip_name'] = ip_name


def xlsx_process_molecule_indication_mapping():
    sheet = ExcelFile.sheet_by_name('Molecule_Indication')
    for x in range(1, sheet.nrows):
        molecule_id = sheet.cell(x, 0).value
        indication_id = sheet.cell(x, 1).value
        clinical_trial_phase = sheet.cell(x, 2).value

        # 创建分子-适应症关系
        molecule_indication_rel_list = molecule_rel_dict['indication']
        molecule_indication_rel_list.append(
            [molecule_id, indication_id, {'clinical_trial_phase': clinical_trial_phase}]
        )


def xlsx_process_molecule_company_mapping():
    sheet = ExcelFile.sheet_by_name('Molecule_Company')
    for x in range(1, sheet.nrows):
        molecule_id = sheet.cell(x, 0).value
        company_id = sheet.cell(x, 1).value

        # 创建分子-公司关系
        molecule_company_rel_list = molecule_rel_dict['company']
        molecule_company_rel_list.append(
            [molecule_id, company_id, {}]
        )


def xlsx_process_molecule_person_mapping():
    sheet = ExcelFile.sheet_by_name('Molecule_Person')
    for x in range(1, sheet.nrows):
        molecule_id = sheet.cell(x, 0).value
        person_id = sheet.cell(x, 1).value

        # 创建分子-人物关系
        molecule_person_rel_list = molecule_rel_dict['person']
        molecule_person_rel_list.append(
            [molecule_id, person_id, {}]
        )


def xlsx_process_molecule_ip_mapping():
    sheet = ExcelFile.sheet_by_name('Molecule_Ip')
    for x in range(1, sheet.nrows):
        molecule_id = sheet.cell(x, 0).value
        ip_id = sheet.cell(x, 1).value

        # 创建分子-专利关系
        molecule_ip_rel_list = molecule_rel_dict['IP']
        molecule_ip_rel_list.append(
            [molecule_id, ip_id, {}]
        )


def xlsx_process_company_ip_mapping():
    sheet = ExcelFile.sheet_by_name('Company_Ip')
    for x in range(1, sheet.nrows):
        company_id = sheet.cell(x, 0).value
        ip_id = sheet.cell(x, 1).value

        # 创建公司-专利关系
        company_ip_rel_list = company_rel_dict['IP']
        company_ip_rel_list.append(
            [company_id, ip_id, {}]
        )


def xlsx_process_company_person_mapping():
    sheet = ExcelFile.sheet_by_name('Company_Person')
    for x in range(1, sheet.nrows):
        company_id = sheet.cell(x, 0).value
        person_id = sheet.cell(x, 1).value

        # 创建公司-人物关系
        company_person_rel_list = company_rel_dict['person']
        company_person_rel_list.append(
            [company_id, person_id, {}]
        )


def xlsx_process_person_ip_mapping():
    sheet = ExcelFile.sheet_by_name('Person_Ip')
    for x in range(1, sheet.nrows):
        person_id = sheet.cell(x, 0).value
        ip_id = sheet.cell(x, 1).value

        # 创建人物-专利关系
        person_ip_rel_list = person_rel_dict['IP']
        person_ip_rel_list.append(
            [person_id, ip_id, {}]
        )


def process():
    kg_dao.reset()

    xlsx_process_company()
    xlsx_process_molecule()
    xlsx_process_person()
    xlsx_process_indication()
    xlsx_process_ip()

    xlsx_process_molecule_indication_mapping()
    xlsx_process_molecule_company_mapping()
    xlsx_process_molecule_person_mapping()
    xlsx_process_molecule_ip_mapping()
    xlsx_process_company_ip_mapping()
    xlsx_process_company_person_mapping()
    xlsx_process_person_ip_mapping()

    # 创建公司节点
    for company_id in company_node_dict:
        company_detail = company_node_dict[company_id]
        company_neo4j_id = kg_dao.create_node(['Company'], company_detail)
        company_detail['id'] = company_neo4j_id
    # 创建分子节点
    for molecule_id in molecule_node_dict:
        molecule_detail = molecule_node_dict[molecule_id]
        molecule_neo4j_id = kg_dao.create_node(['Molecule'], molecule_detail)
        molecule_detail['id'] = molecule_neo4j_id
    # 创建人物节点
    for person_id in person_node_dict:
        person_detail = person_node_dict[person_id]
        person_neo4j_id = kg_dao.create_node(['Person'], person_detail)
        person_detail['id'] = person_neo4j_id
    # 创建适应症节点
    for indication_ip in indication_node_dict:
        indication_detail = indication_node_dict[indication_ip]
        indication_neo4j_id = kg_dao.create_node(['Indication'], indication_detail)
        indication_detail['id'] = indication_neo4j_id
    # 创建IP节点
    for ip_id in ip_node_dict:
        ip_detail = ip_node_dict[ip_id]
        ip_neo4j_id = kg_dao.create_node(['IP'], ip_detail)
        ip_detail['id'] = ip_neo4j_id

    # 创建关系
    # 分子和适应症关系
    molecule_indication_rel_list = molecule_rel_dict['indication']
    for molecule_indication_rel in molecule_indication_rel_list:
        molecule_id = molecule_indication_rel[0]
        if molecule_id not in molecule_node_dict:
            continue
        molecule_neo4j_id = molecule_node_dict[molecule_id]['id']
        indication_id = molecule_indication_rel[1]
        if indication_id not in indication_node_dict:
            continue
        indication_neo4j_id = indication_node_dict[indication_id]['id']
        kg_dao.create_relationship_with_type(molecule_neo4j_id, indication_neo4j_id,
                                             'Molecule_Indication', molecule_indication_rel[2])
    # 分子和公司关系
    molecule_company_rel_list = molecule_rel_dict['company']
    for molecule_company_rel in molecule_company_rel_list:
        molecule_id = molecule_company_rel[0]
        if molecule_id not in molecule_node_dict:
            continue
        molecule_neo4j_id = molecule_node_dict[molecule_id]['id']
        company_id = molecule_company_rel[1]
        if company_id not in company_node_dict:
            continue
        company_neo4j_id = company_node_dict[company_id]['id']
        kg_dao.create_relationship_with_type(molecule_neo4j_id, company_neo4j_id,
                                             'Molecule_Company', molecule_company_rel[2])
    # 分子和人物关系
    molecule_person_rel_list = molecule_rel_dict['person']
    for molecule_person_rel in molecule_person_rel_list:
        molecule_id = molecule_person_rel[0]
        if molecule_id not in molecule_node_dict:
            continue
        molecule_neo4j_id = molecule_node_dict[molecule_id]['id']
        person_id = molecule_person_rel[1]
        if person_id not in person_node_dict:
            continue
        person_neo4j_id = person_node_dict[person_id]['id']
        kg_dao.create_relationship_with_type(molecule_neo4j_id, person_neo4j_id,
                                             'Molecule_Person', molecule_person_rel[2])
    # 分子和专利关系
    molecule_ip_rel_list = molecule_rel_dict['IP']
    for molecule_ip_rel in molecule_ip_rel_list:
        molecule_id = molecule_ip_rel[0]
        if molecule_id not in molecule_node_dict:
            continue
        molecule_neo4j_id = molecule_node_dict[molecule_id]['id']
        ip_id = molecule_ip_rel[1]
        if ip_id not in ip_node_dict:
            continue
        ip_neo4j_id = ip_node_dict[ip_id]['id']
        kg_dao.create_relationship_with_type(molecule_neo4j_id, ip_neo4j_id,
                                             'Molecule_IP', molecule_ip_rel[2])
    # 公司和专利关系
    company_ip_rel_list = company_rel_dict['IP']
    for company_ip_rel in company_ip_rel_list:
        company_id = company_ip_rel[0]
        if company_id not in company_node_dict:
            continue
        company_neo4j_id = company_node_dict[company_id]['id']
        ip_id = company_ip_rel[1]
        if ip_id not in ip_node_dict:
            continue
        ip_neo4j_id = ip_node_dict[ip_id]['id']
        kg_dao.create_relationship_with_type(company_neo4j_id, ip_neo4j_id,
                                             'Company_IP', company_ip_rel[2])
    # 公司和人物关系
    company_person_rel_list = company_rel_dict['IP']
    for company_person_rel in company_person_rel_list:
        company_id = company_person_rel[0]
        if company_id not in company_node_dict:
            continue
        company_neo4j_id = company_node_dict[company_id]['id']
        person_id = company_person_rel[1]
        if person_id not in person_node_dict:
            continue
        person_neo4j_id = person_node_dict[person_id]['id']
        kg_dao.create_relationship_with_type(company_neo4j_id, person_neo4j_id,
                                             'Company_Person', company_person_rel[2])
    # 人物和专利关系
    person_ip_rel_list = person_rel_dict['IP']
    for person_ip_rel in person_ip_rel_list:
        person_id = person_ip_rel[0]
        if person_id not in person_node_dict:
            continue
        person_neo4j_id = person_node_dict[person_id]['id']
        ip_id = person_ip_rel[1]
        if ip_id not in ip_node_dict:
            continue
        ip_neo4j_id = ip_node_dict[ip_id]['id']
        kg_dao.create_relationship_with_type(person_neo4j_id, ip_neo4j_id,
                                             'Person_IP', person_ip_rel[2])


if __name__ == '__main__':
    process()
    kg_dao.close()
