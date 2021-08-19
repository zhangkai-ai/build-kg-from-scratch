import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import org.neo4j.graphdb.Label;
import org.neo4j.unsafe.batchinsert.BatchInserter;
import org.neo4j.unsafe.batchinsert.BatchInserters;

import java.io.*;
import java.util.*;


public class CommonImporter {
    private String nodeDir = "./node.json";
    private String nodeIdDir = "./node_id.json";
    private String outputPath = "./graph.db";

    private void generateKG(){
        String lineStr = null;
        int lineCount = 0;
        BatchInserter inserter = null;
        try{
            inserter = BatchInserters.inserter(new File(outputPath).getAbsoluteFile());
            OutputStreamWriter nodeOut = new OutputStreamWriter(
                    new FileOutputStream(new File(nodeIdDir), false));
            BufferedReader bufferedReader = new BufferedReader(
                    new InputStreamReader(new FileInputStream(nodeDir), "UTF-8"));
            while ((lineStr = bufferedReader.readLine()) != null) {
                lineCount ++;
                Map<String, Object> properties = new HashMap<>();
                Label[] labelArray =  new Label[]{};
                JSONObject propertyJson = JSON.parseObject(lineStr);
                for(Map.Entry entry:propertyJson.entrySet()){
                    String propertyKey = (String)entry.getKey();
                    Object propertyValue = entry.getValue();
                    if(propertyKey.equals("label")){
                        List<Label> labelList = new ArrayList<>();
                        for (Object singleValue:(JSONArray)propertyValue) {
                            labelList.add(Label.label((String)singleValue));
                        }
                        labelArray = new Label[labelList.size()];
                        labelList.toArray(labelArray);
                    }else{
                        if (propertyValue instanceof String){
                            properties.put(propertyKey, propertyValue);
                        }else{
                            List<String> valueList = new ArrayList<>();
                            for (Object singleValue:(JSONArray)propertyValue) {
                                valueList.add((String)singleValue);
                            }
                            String[] valueArray = new String[valueList.size()];
                            valueList.toArray(valueArray);
                            properties.put((String) entry.getKey(), valueArray);
                        }
                    }
                }

                long nodeId = inserter.createNode(properties, labelArray);
                nodeOut.write(nodeId + "\n");
            }
            nodeOut.close();
        }catch (Exception e){
            e.printStackTrace();
            System.out.println("Error text: " + lineStr);
            System.out.println("Error line: " + lineCount);
        }finally{
            if ( inserter != null ) {
                inserter.shutdown();
            }
        }
    }


    public static void main(String[] args){
        CommonImporter test = new CommonImporter();
        test.generateKG();
    }
}
