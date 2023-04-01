package reducers;

import java.io.IOException;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class JobReducer extends Reducer<Text, Text, Text, IntWritable>{

	@Override
	protected void reduce(Text key, Iterable<Text> values, Reducer<Text, Text, Text, IntWritable>.Context context) throws IOException, InterruptedException {
		int countPos = 0;
		int countNeg = 0;
		int countNeu = 0;
		// for loop to count the amount of sentiments for a selected job
		for(Text senti: values) {
			if (senti.toString().equals("neutral")) {
				countNeu ++;
			} else if (senti.toString().equals("positive")) {
				countPos ++;
			} else {
				countNeg ++;
			}
		}
		context.write(new Text(key.toString() + " Positive:"), new IntWritable(countPos));
		context.write(new Text(key.toString() + " Negative:"), new IntWritable(countNeg));
		context.write(new Text(key.toString() + " Neutral:"), new IntWritable(countNeu));
	}
}
