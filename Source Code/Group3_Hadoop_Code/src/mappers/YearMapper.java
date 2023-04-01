package mappers;

import java.io.IOException;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class YearMapper extends Mapper<Text, Text, Text, Text> {
    @Override
    protected void map(Text key, Text value, Mapper<Text, Text, Text, Text>.Context context)
            throws IOException, InterruptedException {
        String[] parts = value.toString().split(",");
        // get the date of the review
        String[] dateStr = parts[5].split("\\s+");
        String[] diffKey = key.toString().split("\t");
        try {
        	// puts the prefix and year as the key and sentiment as value
            String year = dateStr[2];
            for (int i = 0; i < diffKey.length; i++) {
                String sentiment = diffKey[i];
                String prefix = (i == 0) ? "UnMatched" : "Matched";
                context.write(new Text(prefix + "\t" + year), new Text(sentiment));
            }
        } catch (ArrayIndexOutOfBoundsException ex) {
        	System.out.println(parts[5]);
//            System.out.println("Out of Bounds");
        }
    }
}