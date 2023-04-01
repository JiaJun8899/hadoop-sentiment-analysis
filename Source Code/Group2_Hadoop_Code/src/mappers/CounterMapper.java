package mappers;
import java.io.IOException;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class CounterMapper extends Mapper<Text, Text, Text, Text>{

	@Override
	protected void map(Text key, Text value, Mapper<Text, Text, Text, Text>.Context context) throws IOException, InterruptedException {
		String[] diffKey = key.toString().split("\t");
		String[] parts = value.toString().split(",");
		String[] pros = parts[3].split("\\s+");
		String[] cons = parts[4].split("\\s+");
		if(diffKey[0].equals("positive")) {
			for (String w: pros) {
				context.write(new Text("UnMatched\t" + diffKey[0]), new Text("pros\t" + w));
			}
			for (String w: cons) {
				context.write(new Text("UnMatched\t" + diffKey[0]), new Text("cons\t" + w));
			}
		}
		if(diffKey[0].equals("negative")) {
			for (String w: pros) {
				context.write(new Text("UnMatched\t" + diffKey[0]), new Text("pros\t" + w));
			}
			for (String w: cons) {
				context.write(new Text("UnMatched\t" + diffKey[0]), new Text("cons\t" + w));
			}
		}
		if(diffKey[0].equals("neutral")) {
			for (String w: pros) {
				context.write(new Text("UnMatched\t" + diffKey[0]), new Text("pros\t" + w));
			}
			for (String w: cons) {
				context.write(new Text("UnMatched\t" + diffKey[0]), new Text("cons\t" + w));
			}
		}
		if(diffKey[1].equals("positive")) {
			for (String w: pros) {
				context.write(new Text("Matched\t" + diffKey[0]), new Text("pros\t" + w));
			}
			for (String w: cons) {
				context.write(new Text("Matched\t" + diffKey[0]), new Text("cons\t" + w));
			}
		}
		if(diffKey[1].equals("negative")) {
			for (String w: pros) {
				context.write(new Text("Matched\t" + diffKey[0]), new Text("pros\t" + w));
			}
			for (String w: cons) {
				context.write(new Text("Matched\t" + diffKey[0]), new Text("cons\t" + w));
			}
		}
		if(diffKey[1].equals("neutral")) {
			for (String w: pros) {
				context.write(new Text("Matched\t" + diffKey[0]), new Text("pros\t" + w));
			}
			for (String w: cons) {
				context.write(new Text("Matched\t" + diffKey[0]), new Text("cons\t" + w));
			}
		}
	}
}
