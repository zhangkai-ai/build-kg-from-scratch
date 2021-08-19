from agdistispy.agdistis import Agdistis
# 使用Agdistis官方python包完成实体链接任务
ag = Agdistis()
result = ag.disambiguate("After unsuccessful years, aging country star <entity>Jonny Cash</entity> made a grandiose comeback with his <entity>American Recordings<\entity>, recorded at his home with the help of <entity>Rick Rubin</entity>.")
print(result)

# 启动中文Agdistis后，请求本地服务
import json
import requests
result = requests.post("http://localhost:8080/AGDISTIS", data={"text": "<entity>北京</entity>和<entity>上海</entity>分别是<entity>中国</entity>的政治和经济中心"})
print(json.loads(result.text))
