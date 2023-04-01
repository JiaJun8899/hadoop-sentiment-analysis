package mappers;

import java.io.IOException;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class JobMapper extends Mapper<Text, Text, Text, Text> {

	@Override
	protected void map(Text key, Text value, Mapper<Text, Text, Text, Text>.Context context)
			throws IOException, InterruptedException {
		String[] parts = value.toString().split(",");
		String job = parts[1];
		String[] diffKey = key.toString().split("\t");
		if (diffKey[0].equals("positive")) {
			context.write(new Text("UnMatched\t" + job), new Text(diffKey[0]));
		}
		if (diffKey[0].equals("negative")) {
			context.write(new Text("UnMatched\t" + job), new Text(diffKey[0]));
		}
		if (diffKey[0].equals("neutral")) {
			context.write(new Text("UnMatched\t" + job), new Text(diffKey[0]));
		}
		if (diffKey[1].equals("positive")) {
			context.write(new Text("Matched\t" + job), new Text(diffKey[0]));
		}
		if (diffKey[1].equals("negative")) {
			context.write(new Text("Matched\t" + job), new Text(diffKey[1]));
		}
		if (diffKey[1].equals("neutral")) {
			context.write(new Text("Matched\t" + job), new Text(diffKey[0]));
		}
	}
}
