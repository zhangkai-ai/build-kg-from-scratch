#!/usr/bin/env python
# -*- coding:utf8 -*-

reg_body_name = "头发|毛发|眼睛|瞳孔"
reg_end_word = "也|不|给|的|吗|家|了|么|呀|吧|来|哪|连|阿|呢|啦|则|哇|哈|咧|啊|哩|呗|罗|价|喽|呵|般|否|耶|哉|罢|呕|咯|嘛|噢|哟|呐|呦|啰"
punctuation = "\\.|。|,|，|？|\\?|!|！"
reg_what = "(什么|吗|对吧|是吧|啥|嘛|多少|多大|多高|什么类型|什么类别|什么样|怎么样|怎样|如何|几岁|几号|哪个|哪一个|哪里|哪几个|哪个|哪种|哪一种|哪些|哪里|哪一部|哪部|哪类|哪|哪款|几种|哪一|哪家|(是.+还是.+)|是男是女|知道吗|知道么|知道不|猜的?到吗|猜的?出来吗)"
reg_constellation = "(双子|双鱼|处女|天秤|天蝎|射手|巨蟹|摩羯|水瓶|狮子|白羊|金牛)"
reg_mother = "妈妈|老妈|娘|老娘|母亲|母上|妈咪"
reg_father = "爸爸|老子|爹|老汉|老爸|父亲|家父"
reg_blood = "(rh阴性?血?|熊猫|ab|AB|a|A|b|B|o|O|阴)"
reg_male = "((成年|青年|幼年|老年|壮年)?(大叔|雄性|汉子|小伙子|少爷|爷们|纯爷们|帅哥|你哥|公子|男神|男生|男性|男人|男|绅士|小鲜肉|小男孩))"
reg_ad_male = "(有把的?|带把的?|有小鸡鸡的?|下半身思考的?|荷尔蒙动物)"
reg_female = "(成年|青年|幼年|老年|壮年)?(女性|女生|女神|女的|女|雌性|妹子|姑娘|美女|妹子|妹纸|萌妹纸|萌妹子|软妹|软妹纸|软妹子|女神|小姐|母|女子|宫|御姐)"
reg_ad_female = '(没把|没有把|木有把|没带把|没有小鸡鸡|木有小鸡鸡|能生孩子|有胸)'
reg_tone = "(吗|嘛|么|啊|呀|哈|(是.+还是.+))"
reg_verb = "成立|创办|出版|出生|实施|上市|发布|上线|隶属|死亡|去世|逝世|诞辰|亡故|死|起源|上学|所处|处于|出土|出处|在位|发生|批准|创作|定型|现藏|更名|签署|拍摄|申报|组建|原产|发射|施行|修建|修订|开业|形成|始建|发行|建立|司职|执教|曾执教|创立|测试|通车"
reg_sex_man = "男|汉子"
reg_sex_woman = "女|妹子"
reg_how_end = "吗|对吧|是吧"
CN_NUM = {
    '〇': 0,
    '一': 1,
    '二': 2,
    '三': 3,
    '四': 4,
    '五': 5,
    '六': 6,
    '七': 7,
    '八': 8,
    '九': 9,

    '零': 0,
    '壹': 1,
    '贰': 2,
    '叁': 3,
    '肆': 4,
    '伍': 5,
    '陆': 6,
    '柒': 7,
    '捌': 8,
    '玖': 9,

    '貮': 2,
    '两': 2,
}
CN_UNIT = {
    '十': 10,
    '拾': 10,
    '百': 100,
    '佰': 100,
    '千': 1000,
    '仟': 1000,
    '万': 10000,
    '萬': 10000,
    '亿': 100000000,
    '億': 100000000,
    '兆': 1000000000000,
}


def cn2dig(cn):
    #四十
    ldig = ""  # 临时字符串
    tail_len = 0
    for i in range(len(cn)):
        cndig = cn[i] #四
        if 0 == i and '十' == cndig:
            ldig = ldig + '1'
        elif cndig in CN_UNIT:
            tail_len = len(str(CN_UNIT[cndig])) - 1
            continue
        elif cndig in CN_NUM:
            unit = CN_NUM.get(cndig) #4
            ldig = ldig + str(unit) #4
            tail_len = tail_len - 1 #-1
        else:
            if tail_len > 0:
                ldig = ldig + '0' * tail_len
                tail_len = 0
            ldig = ldig + cndig
    if tail_len ==0:
        return ldig
    else:
        return ldig + tail_len*"0"


attributes_order={"gender":"1", "age":"2", "birthDate":"3", "deathDate":"3", "constellation":"5", "sports_team":"100", "bloodType":"6","nationality":"7", "birthPlace":"8", "height":"9","weight":"10", "achievement":"12", "honor":"28",
                  "works":"14", "spouse":"11", "famous_alumi":"16", "school_address":"16","true_name":"16","construction_area":"16", "company_name":"16", "school_code": "16", "school_song": "16", "master_point": "16", "friend":"16", "parent":"17", "children":"18", "brother_sister":"19","alias":"20", "ethnic":"21", "graduate_school":"23", "education":"22", "faith":"24", "nativePlace":"25",
                  "position":"26", "BWH":"27","jobTitle":"1000000","headquarters_location":"101", "business_scope":"103", "nature":"104","company_slogan":"105", "employee_number":"106",
                  "annual_turnover":"107", "registered_capital":"108","chairman":"109", "founder":"102", "total_assets": "111", "time2market": "112", "stock_code":"113","brand":"114",
                  "uptime":"116", "management_idea":"117", "product": "118","enterprise_spirit":"119","type":"120", "author": "201", "booktitle":"202", "press": "203","publish_time":"204", "feature":"205", "booksize":"206",
                  "binding":"207", "page_number": "208","translator": "209", "word_number": "210", "paper_type": "211", "edition":"212", "building_name": "213","price":"214", "area":"215", "developer": "216",
                  "address": "218","city": "219", "subject": "220", "green_rate": "221", "architectural_form":"222", "FAR": "223","property_fee":"224", "house_number": "225", "house_price": "226",
                  "room_time": "227", "animal_type": "228","distribution_area":"229", "purpose": "230", "attribute": "231","abbreviation":"232", "full_name": "233","definition":"234", "application":"235", "official_network":"236",
                  "administrative_division":"237", "field": "238","subjection": "239", "content": "240", "include": "241", "predecessor": "243", "status": "244", "website_name": "245", "source": "246", "pos": "247",
                  "reason":"248", "population": "249", "background": "250", "implement_time": "251", "principle":"252", "releaseUnit":"253", "harmfulPart":"254", "effect": "256", "person":"257",
                  "competent_department":"258", "core":"259", "idea":"260", "model":"261", "function":"262", "climatic_conditions":"263", "business":"264", "reference_number":"265","theory": "266"}


attributes_dict = {"性别":"gender", "年龄": "age", "出生日期":"birthDate", "死亡日期":"deathDate", "星座":"constellation", "职业":"jobTitle", "血型":"bloodType",
                   "出生地":"birthPlace", "身高":"height", "体重":"weight", "父母": "parent", "母亲":"mother", "父亲":"father", "主要成就":"achievement",
                   "朋友":"friend", "别名":"alias", "民族":"ethnic", "毕业院校":"graduate_school", "国籍":"nationality","学历":"education", "信仰":"faith",
                   "籍贯": "nativePlace", "职务":"position", "三围":"BWH", "代表作品":"works", "荣誉":"honor", "妻子":"spouse", "孩子":"children", "兄妹":"brother_sister",
                   "总部地点":"headquarters_location", "经营范围":"business_scope", "公司性质":"nature", "公司口号":"company_slogan", "员工数":"employee_number" ,
                   "年营业额":"annual_turnover", "注册资本":"registered_capital", "董事长":"chairman", "创始人":"founder", "总资产":"total_assets",
                   "上市时间":"time2market", "股票代码":"stock_code",  "品牌":"brand", "法定代表人":"legal_representative", "发布时间":"uptime", "经营理念":"management_idea",
                   "产品":"product", "企业精神":"enterprise_spirit", "类型":"type", "作者":"author", "书名":"booktitle", "出版社":"press", "出版时间":"publish_time",
                   "特点":"feature", "开本":"booksize", "装帧":"binding", "页数":"page_number", "译者":"translator", "字数":"word_number", "纸张":"paper_type",
                   "版次":"edition", "楼盘名":"building_name", "定价":"price", "面积":"area", "开发商":"developer", "物业类别":"property_company_type",
                   "楼盘地址":"address", "城区":"city", "学科":"subject", "绿化率":"green_rate", "建筑形式":"architectural_form", "容积率":"FAR", "物业费":"property_fee",
                   "总户数":"house_number", "均价":"house_price", "交房时间":"room_time", "界":"animal_type", "分布区域":"distribution_area", "目的":"purpose",
                   "属性":"attribute", "简称":"abbreviation", "全称":"full_name", "定义":"abstract", "作用":"application", "官网":"official_network",
                   "行政区域":"administrative_division", "领域":"field", "隶属":"subjection", "内容":"content", "实质":"essence", "前身":"predecessor",
                   "地位":"status", "网站名称":"website_name", "来源":"source", "词性":"pos", "人口":"population", "成立时间":"establish_time", "背景":"background",
                   "原因":"reason", "实施时间":"implement_time", "英文名称":"foreignName", "包括":"include", "原则":"principle", "发布单位":"releaseUnit",
                   "为害部位":"harmfulPart", "行政区类别":"Administrative_category", "影响":"effect", "人物":"person", "主管部门":"competent_department",
                   "核心":"core", "理念":"idea", "型号":"model", "职能":"function", "气候条件":"climatic_conditions", "业务":"business", "文号":"reference_number",
                   "行业":"industry", "屏幕尺寸":"screen_size", "电话区号":"telephone_code", "车牌代码":"plate_number", "主要院系":"major_college", "原理":"theory",
                   "方言":"dialect", "级别":"level", "产权年限":"propertyYear", "机场":"airPort", "校训":"schoolMotto", "邮政区码":"zipCode", "熔点":"meltingPoint",
                   "著名景点":"viewSpot", "现任校长":"Principal"}

attributes_regex = "性别|年龄|年纪|岁数|生日|出生日期|逝世日期|忌日|去世时间|星座|工作|职业|工种|血型|血液|祖国|国籍|国家|老家|祖籍|出生地|身高|高度|体重|重量|成就|父母|朋友|小名|别名|代称|别称|民族|毕业学校|毕业院校|学历|教育|最高学历|信仰|户口|籍贯|\
                   |户籍|父亲|母亲|户口所在|职称|官职|作品|职务|三围|腰围|臀围|胸围|总部地点|总部地址|总部所在地|总部|经营范围|经营的范围|性质|口号|员工数量|员工人数|年营业额|注册资本|注册资金|董事长|创始人|总资产|股票代码|证券代码|品牌|法定代表人|法人代表|\
                   |上线|发布|经营理念|产品|企业精神|公司精神|企业类型|公司类型|类型|作者|写的|类别|书名|出版社|出版时间|特点|特色|特征|优点|优势|开本|装帧|页数|译者|字数|纸张类型|版本|版次|楼盘名称|楼盘名|定价|价格|面积|开发商|楼盘|物业|地址|城市|城区|学科|\
                   |绿化率|建筑形式|容积率|物业费|户数|房价|交房|分布区域|生活区域|区域|科目|纲目|目的|属性|简称|全称|地点|所在地|定义|含义|概念|简介|释义|意思|功效|效果|作用|官网|官方网站|行政区域|领域|隶属|内容|组成|本质|实质|宗旨|应用|前身|用途|网站名称|\
                   |来源|词性|词性|原因|人口|背景|实施|理念|职能"

general_pattern = "哪里|什么|哪一位|哪位|哪一样|哪几个|哪一个|哪个|哪"