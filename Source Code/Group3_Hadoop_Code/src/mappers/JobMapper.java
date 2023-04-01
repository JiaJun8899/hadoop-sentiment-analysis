package mappers;

import java.io.IOException;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class JobMapper extends Mapper<Text, Text, Text, Text> {
    @Override
    protected void map(Text key, Text value, Mapper<Text, Text, Text, Text>.Context context)
            throws IOException, InterruptedException {
        String[] parts = value.toString().split(",");
        //get the job title
        String job = parts[1];
		// index [0] is unmatched and [1] is matched
        String[] diffKey = key.toString().split("\t");
        // loop to write the prefix and puts the job as key and sentiment as value
        for (int i = 0; i < diffKey.length; i++) {
            String sentiment = diffKey[i];
            String prefix = (i == 0) ? "UnMatched" : "Matched";
            context.write(new Text(prefix + "\t" + job), new Text(sentiment));
        }
    }
}