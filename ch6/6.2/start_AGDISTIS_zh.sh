# 下载中文知识库索引文件
wget https://hobbitdata.informatik.uni-leipzig.de/agdistis/dbpedia_index_2016-10/index_zh.zip
# 解压索引文件
unzip index_zh.zip
# 获取AGDISTIS源码
git clone https://github.com/dice-group/AGDISTIS.git
# 进入目录
cd AGDISTIS
# 拷贝索引文件
cp -r ../index_zh ./index
# 使用修改过的代码替换源文件，以获得正确的url
cp ../GetDisambiguation.java ./src/main/java/org/aksw/agdistis/webapp/GetDisambiguation.java
# 启动AGDISTIS服务，需要提前安装Maven
mvn -Dmaven.tomcat.port=8080 tomcat:run
# 测试该服务
# curl --data-urlencode "text='<entity>北京</entity>和<entity>上海</entity>是<entity>中国</entity>的主要城市。'" -d type='agdistis' http://localhost:8181/AGDISTIS