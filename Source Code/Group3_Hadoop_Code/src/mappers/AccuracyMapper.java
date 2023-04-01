package mappers;

import java.io.IOException;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class AccuracyMapper extends Mapper<Text, Text, Text, Text> {

	@Override
	protected void map(Text key, Text value, Mapper<Text, Text, Text, Text>.Context context)
			throws IOException, InterruptedException {
		//splits the data into the different parts 
		String[] parts = value.toString().split(",");
		try {
			// take the actual rating
			Double rating = Double.parseDouble(parts[2]);
			// index [0] is unmatched and [1] is matched
			String[] diffKey = key.toString().split("\t");
			// get the actual sentiment of the review based on the user
			String sentiment;
			if (rating == 3.0) {
				sentiment = "neutral";
			} else if (rating > 3.0) {
				sentiment = "positive";
			} else {
				sentiment = "negative";
			}
			context.write(new Text("UnMatched"), new Text(rating + "\t" + sentiment + "\t" + diffKey[0]));
			context.write(new Text("Matched"), new Text(rating + "\t" + sentiment + "\t" + diffKey[1]));
		} catch (NumberFormatException ex) {
			System.out.println("Format issue");
		}
	}
}
