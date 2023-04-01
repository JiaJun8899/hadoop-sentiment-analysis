package reducers;
import java.io.IOException;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class YearReducer extends Reducer<Text, Text, Text, IntWritable>{

	@Override
	protected void reduce(Text key, Iterable<Text> values, Reducer<Text, Text, Text, IntWritable>.Context context) throws IOException, InterruptedException {
		int posCount = 0;
		int neuCount = 0;
		int negCount = 0;
		int totalYear = 0;
		// counts the sentiments for the unique year that is in the dataset
		for (Text value: values) {
			String sentiment = value.toString();
			if (sentiment.equals("positive")) {
				posCount ++;
			}
			if (sentiment.equals("negative")) {
				negCount ++;
			}
			if (sentiment.equals("neutral")) {
				neuCount++;
			}
			totalYear++;
		}
		context.write(new Text(key.toString() + " Positive:"), new IntWritable(posCount));
		context.write(new Text(key.toString() + " Negative:"), new IntWritable(negCount));
		context.write(new Text(key.toString() + " Neutral:"), new IntWritable(neuCount));
		context.write(new Text(key.toString() + " Total:"), new IntWritable(totalYear));
	}
	
}
