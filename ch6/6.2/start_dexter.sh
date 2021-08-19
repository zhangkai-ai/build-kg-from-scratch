# 下载并解压dexter安装包
wget http://hpc.isti.cnr.it/~ceccarelli/dexter2.tar.gz
tar -xvzf dexter2.tar.gz
# 进入目录
cd dexter2
# 启动dexter服务
java -Xmx4000m -jar dexter-2.1.0.jar
# 测试
# curl http://localhost:8080/dexter-webapp/api/rest/annotate?text=After%20unsuccessful%20years,%20aging%20country%20star%20Jonny%20Cash%20made%20a%20grandiose%20comeback%20with%20his%20American%20Recordings,%20recorded%20at%20his%20home%20with%20the%20help%20of%20Rick%20Rubin.&n=50&wn=false&debug=false&format=text&min-conf=0.8