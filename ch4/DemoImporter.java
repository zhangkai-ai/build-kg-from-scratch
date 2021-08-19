import org.neo4j.graphdb.Label;
import org.neo4j.unsafe.batchinsert.BatchInserter;
import org.neo4j.unsafe.batchinsert.BatchInserters;

import java.io.File;
import java.util.HashMap;
import java.util.Map;

public class DemoImporter {
    private void generateSampleKG(){
        String outputPath = "./graph.db";

        Map<String, Object> properties = new HashMap<String, Object>(){{
                put("name", "北京小米科技有限责任公司");
                put("url_name", "北京小米科技有限责任公司");
                put("url_id", "3250213");
                put("disambiguation", new String[]{"小米公司"});
                put("成立时间", "2010-3");
                put("公司口号", new String[]{"小米为发烧而生", "探索黑科技"});
            }
        };
        Label[] labelArray =  new Label[]{Label.label("Entity")};

        BatchInserter inserter = null;
        try{
            inserter = BatchInserters.inserter(new File(outputPath).getAbsoluteFile());
            long nodeId = inserter.createNode(properties, labelArray);
        }catch (Exception e){
            e.printStackTrace();
        }finally {
            if ( inserter != null ) {
                inserter.shutdown();
            }
        }
    }

    public static void main(String[] args){
        DemoImporter demoImporterTest = new DemoImporter();
        demoImporterTest.generateSampleKG();
    }
}