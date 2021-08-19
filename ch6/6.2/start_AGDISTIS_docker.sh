# 拉取agdistis docker镜像
docker pull aksw/agdistis
# 下载英文index和index by context数据
wget https://hobbitdata.informatik.uni-leipzig.de/agdistis/dbpedia_index_2016-04/en/indexdbpedia_en_2016.zip
unzip indexdbpedia_en_2016.zip
wget https://hobbitdata.informatik.uni-leipzig.de/agdistis/dbpedia_index_2016-04/en/index_bycontext.zip
unzip index_bycontext.zip
# 启动agdistis容器
docker run -d --name agdistis -v `pwd`/indexdbpedia_en_2016:/usr/local/tomcat/index -v `pwd`/index_bycontext:/usr/local/tomcat/index_bycontext -p 8080:8080 -e AGDISTIS_NODE_TYPE=http://dbpedia.org/resource/ -e AGDISTIS_EDGE_TYPE=http://dbpedia.org/ontology/ -e AGDISTIS_BASE_URI=http://dbpedia.org aksw/agdistis:latest
# 测试
curl --data-urlencode "text='The <entity>University of Leipzig</entity> in <entity>Leipzig</entity>.'" -d type='agdistis' http://localhost:8080/AGDISTIS