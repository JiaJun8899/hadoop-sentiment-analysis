package mappers;

import java.io.IOException;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class AccuracyMapper extends Mapper<Text, Text, Text, Text> {

	@Override
	protected void map(Text key, Text value, Mapper<Text, Text, Text, Text>.Context context)
			throws IOException, InterruptedException {
		String[] parts = value.toString().split(",");
		try {
			Double rating = Double.parseDouble(parts[2]);
			String[] diffKey = key.toString().split("\t");
			if (rating == 3.0) {
				context.write(new Text("UnMatched"), new Text(rating + "\tneutral\t" + diffKey[0]));
				context.write(new Text("Matched"), new Text(rating + "\tneutral\t" + diffKey[1]));
			}
			if (rating > 3.0) {
				context.write(new Text("UnMatched"), new Text(rating + "\tpositive\t" + diffKey[0]));
				context.write(new Text("Matched"), new Text(rating + "\tpositive\t" + diffKey[1]));
			}
			if (rating < 3.0) {
				context.write(new Text("UnMatched"), new Text(rating + "\tnegative\t" + diffKey[0]));
				context.write(new Text("Matched"), new Text(rating + "\tnegative\t" + diffKey[1]));
			}
		} catch (NumberFormatException ex) {
			System.out.println("Format issue");
		}
	}

}
