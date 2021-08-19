import json
import time
import random
import copy
import requests
import datetime
from filter.topic_filter import add_entity_topic

template_dict = {}
template_dict.update(json.loads(open('data/nlg/general.json').read()))
template_dict.update(json.loads(open('data/nlg/work.json').read()))
template_dict.update(json.loads(open('data/nlg/relax.json').read()))
variable_dict = json.loads(open('data/nlg/variable.json').read())
for variable_name in variable_dict:
    raw_str = variable_dict[variable_name]
    variable_dict[variable_name] = raw_str.split('|')

play_detail_topic = json.loads(open('data/topic/play_details_topic.json').read())

play_detail_comments = json.loads(open('data/topic_reply/play_detail_comments.json').read())


def test_all():
    '''
    批量验证模板生成的正确性
    :return:
    '''
    for event_name in template_dict:
        detail_dict = template_dict[event_name]
        for time_type in detail_dict:
            for template in detail_dict[time_type]:
                if time_type == 'past':
                    template = template.replace('[time]', '上午')
                if time_type == 'will':
                    template = template.replace('[time]', '晚上9点')
                print(template)
                response = ''
                i = 0
                while i < len(template):
                    # replace variable
                    if template[i] == '{':
                        end_pos = template.index('}', i+1)
                        variable_name = template[i+1:end_pos]
                        word_list = copy.deepcopy(variable_dict[variable_name])
                        if end_pos+1 < len(template) and template[end_pos+1] == '?':
                            word_list.append('')
                            i = end_pos + 2
                        else:
                            i = end_pos + 1
                        response += random.choice(word_list)
                    elif template[i] == '(':
                        end_pos = template.index(')', i + 1)
                        word_list = [template[i + 1:end_pos]]
                        if end_pos+1 < len(template) and template[end_pos+1] == '?':
                            word_list.append('')
                            i = end_pos + 2
                        else:
                            i = end_pos + 1
                        response += random.choice(word_list)
                    else:
                        if i+1 < len(template) and template[i+1] == '?':
                            word_list = [template[i], '']
                            response += random.choice(word_list)
                            i += 2
                        else:
                            response += template[i]
                            i += 1
                print(response)
                print()


# 获取16号那天的时间戳
now_time = int(time.time())  # 当前时间戳
today_data = str(datetime.date.today())  # 当前日期
today_strptime = time.strptime(today_data, "%Y-%m-%d")
today_strptime = int(time.mktime(today_strptime))
diff_time = now_time - today_strptime  # 当天时间戳之差
sixteen_date_time = 1565884800   # 16号0点时间戳
sixteen_date_now_time = sixteen_date_time + diff_time  # 16号时间戳


def generate(slot_dict):
    '''
    生成琥珀相关的事件描述回复，调用data/nlg模板，进行生成，生成过程：1.选择事件 2.选择时间 3.随机选择模板 4.随机填充模板变量 5.填充槽位
    :param slot_dict: 槽位字典
    :return:琥珀相关的事件描述回复
    '''
    detail_dict = template_dict[slot_dict['type']]
    type_class = slot_dict['type']
    # now_time = time.time()
    # now_time = sixteen_date_now_time
    event_begin_time = slot_dict['begin_time']
    event_end_time = slot_dict['end_time']
    opinion = slot_dict['reply']
    if sixteen_date_now_time > event_end_time:
        template = random.choice(detail_dict['past'])
        template = template.replace('[time]', time_nlg(event_begin_time, type_class, False))
    elif sixteen_date_now_time < event_begin_time:
        template = random.choice(detail_dict['will'])
        template = template.replace('[time]', time_nlg(event_begin_time, ''))
        opinion = ''
    else:
        template = random.choice(detail_dict['now'])
    # print(template)
    response = ''
    i = 0
    while i < len(template):
        # replace variable
        if template[i] == '{':
            end_pos = template.index('}', i + 1)
            variable_name = template[i + 1:end_pos]
            word_list = copy.deepcopy(variable_dict[variable_name])
            if end_pos + 1 < len(template) and template[end_pos + 1] == '?':
                word_list.append('')
                i = end_pos + 2
            else:
                i = end_pos + 1
            response += random.choice(word_list)
        elif template[i] == '(':
            end_pos = template.index(')', i + 1)
            word_list = [template[i + 1:end_pos]]
            if end_pos + 1 < len(template) and template[end_pos + 1] == '?':
                word_list.append('')
                i = end_pos + 2
            else:
                i = end_pos + 1
            response += random.choice(word_list)
        else:
            if i + 1 < len(template) and template[i + 1] == '?':
                word_list = [template[i], '']
                response += random.choice(word_list)
                i += 2
            else:
                response += template[i]
                i += 1
    slot_list = ['name', 'sub_type', 'author']
    for slot_name in slot_list:
        pattern = '[{}]'.format(slot_name)
        if pattern in response:
            if slot_name == 'author':
                authors = slot_dict[slot_name]
                if len(authors) >= 2:
                    author = authors[0] + '等人'
                elif len(authors) == 1:
                    author = authors[0]
                else:
                    author = ''
                response = response.replace(pattern, author)
            else:
                response = response.replace(pattern, slot_dict[slot_name])
    if opinion:
        response = '{}。{}'.format(response, opinion)
    return response


def time_nlg(time_stamp, type_class, specific=True):
    '''
    将时间戳格式，转化为文字表述形式输出，该函数仅输出当日的时间，如"上午9点15"
    :param time_stamp: 时间戳
    :param specific: 是否输出具体的时间，默认输出，否则仅输出早上、下午、晚上
    :return: 时间表述
    '''
    response = ''
    # day_today = int(time.strftime("%d", time.localtime(time.time())))
    day_today = 16
    day = int(time.strftime("%d", time.localtime(time_stamp)))
    day_shift = day_today - day
    hour = int(time.strftime("%H", time.localtime(time_stamp)))
    minute = int(time.strftime("%M", time.localtime(time_stamp)))
    if minute == 0:
        minute = ''
    if hour > 18:
        if type_class == 'meal':
            if day_shift == 0:
                hour -= 12
                if specific:
                    response = '今天{}点{}'.format(hour, minute)
                else:
                    response = '今天'
            elif day_shift == 1:
                response = '昨天'
            elif day_shift == 2:
                response = '前天'
        else:
            if day_shift == 0:
                hour -= 12
                if specific:
                    response = '晚上{}点{}'.format(hour, minute)
                else:
                    response = '晚上'
            elif day_shift == 1:
                response = '昨天晚上'
            elif day_shift == 2:
                response = '前天晚上'
    elif hour > 13:
        if type_class == 'meal':
            if day_shift == 0:
                hour -= 12
                if specific:
                    response = '今天{}点{}'.format(hour, minute)
                else:
                    response = '今天'
            elif day_shift == 1:
                response = '昨天'
            elif day_shift == 2:
                response = '前天'
        else:
            if day_shift == 0:
                hour -= 12
                if specific:
                    response = '下午{}点{}'.format(hour, minute)
                else:
                    response = '下午'
            elif day_shift == 1:
                response = '昨天下午'
            elif day_shift == 2:
                response = '前天下午'
    else:
        if type_class == 'meal':
            if day_shift == 0:
                if specific:
                    response = '今天{}点{}'.format(hour, minute)
                else:
                    response = '今天'
            elif day_shift == 1:
                response = '昨天'
            elif day_shift == 2:
                response = '前天'
        else:
            if day_shift == 0:
                if specific:
                    response = '上午{}点{}'.format(hour, minute)
                else:
                    response = '上午'
            elif day_shift == 1:
                response = '昨天上午'
            elif day_shift == 2:
                response = '前天上午'
    return response


def topic_info(candidate_topic):
    amber_24hr_content = add_entity_topic()
    result_dict = {}
    initial_value = 1000000
    for events in amber_24hr_content:
        events_detail = amber_24hr_content[events]
        for event_detail in events_detail:
            event_topic = event_detail['topic']
            if candidate_topic in event_topic:
                if candidate_topic in play_detail_topic:
                    events = play_detail_topic[candidate_topic]
                    event_detail['type'] = events
                    detail_reply = play_detail_comments[events]
                    event_detail['reply'] = random.choice(detail_reply)
                if events in result_dict:
                    result_dict[events].append(event_detail)
                else:
                    result_dict[events] = [event_detail]
    event_info = ''
    for slot in result_dict:
        events_detail = result_dict[slot]
        for event_detail in events_detail:
            begin_time = event_detail['begin_time']
            compare_value = abs(sixteen_date_now_time - begin_time)
            if compare_value < initial_value:
                event_info = generate(event_detail)
                initial_value = compare_value
    return event_info


if __name__ == '__main__':
    # start_time = time.time()
    # slot_test = {
    #     'begin_time': 1565910900-3600*24*2,
    #     'end_time': 1565911800-3600*24*2,
    #     'type': 'book',
    #     'name': '我的前半生',
    #     'sub_type': '文学',
    #     'author': 'xxx',
    #     'reply': '很好看'
    # }
    # rst = generate(slot_test)
    # print(rst)
    # print(time.time()-start_time)
    # test_all()

    test_words = [
        # '上网',
        # '看视频',
        # '看直播',
        # '网上购物',
        '微博',
        # '淘宝',
        # '优酷',
        # '爱奇艺',
        # '闲鱼',
        # '斗鱼',
        # '下棋',
        # '象棋',
        # '军棋',
        # '五子棋',
        # '围棋',
        # '跳棋',
        # '飞行棋',
        # '看报纸杂志',
        # '看经济杂志',
        # '阅读经济杂志',
        # '看时尚杂志',
        # '阅读时尚杂志',
        # '看时事新闻',
        # '阅读时事新闻',
        # '打理花草',
        # '打理多肉植物',
        # '多肉观音莲',
        # '凝脂莲',
        # '打理水生植物',
        # '睡莲',
        # '美人蕉',
        # '打理草本植物',
        # '向日葵',
        # '菊花',
        # '打理室内植物',
        # '紫罗兰',
        # '打理观花植物',
        # '迷迭香'
    ]
    #
    for test_word in test_words:
        res = topic_info(test_word)
        print(res)

    # res = topic_info('下棋')
    # print(res)

    # topic qa test
    # try:
    #     post_data = {
    #         "sent": "今天该出去旅游吗",
    #         "topN": 1
    #     }
    #     rst_dict = requests.post('http://172.27.1.207:13333/topic_qa/', json.dumps(post_data)).json()
    #     print(rst_dict['answers'][0]['reply'])
    #
    # except Exception as e:
    #     print(e)

