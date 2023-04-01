package mappers;
import java.io.IOException;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class CounterMapper extends Mapper<Text, Text, Text, Text> {

    @Override
    protected void map(Text key, Text value, Mapper<Text, Text, Text, Text>.Context context) throws IOException, InterruptedException {
        // index [0] is for unmatched and index [1] is for matched
    	String[] diffKey = key.toString().split("\t");
    	// split into the different parts for analysis
        String[] parts = value.toString().split(",");
        // tokenize the pros and cons
        String[] prosToken = parts[3].split("\\s+");
        String[] consToken = parts[4].split("\\s+");
        
        for (int i = 0; i < diffKey.length; i++) {
            String prefix = (i == 0) ? "UnMatched" : "Matched";
            for (String wordInPro : prosToken) {
                context.write(new Text(prefix + "\t" + diffKey[i]), new Text("pros\t" + wordInPro));
            }
            for (String wordInCon : consToken) {
                context.write(new Text(prefix + "\t" + diffKey[i]), new Text("cons\t" + wordInCon));
            }
        }
    }
}
