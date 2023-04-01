package mappers;

import java.io.IOException;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class YearMapper extends Mapper<Text, Text, Text, Text> {

	@Override
	protected void map(Text key, Text value, Mapper<Text, Text, Text, Text>.Context context)
			throws IOException, InterruptedException {
		String[] parts = value.toString().split(",");
		String[] dateStr = parts[5].split("\\s+");
		String[] diffKey = key.toString().split("\t");
		try {
			String year = dateStr[2];
			if (diffKey[0].equals("positive")) {
				context.write(new Text("UnMatched\t" + year), new Text(diffKey[0]));
			}
			if (diffKey[0].equals("negative")) {
				context.write(new Text("UnMatched\t" + year), new Text(diffKey[0]));
			}
			if (diffKey[0].equals("neutral")) {
				context.write(new Text("UnMatched\t" + year), new Text(diffKey[0]));
			}
			if (diffKey[1].equals("positive")) {
				context.write(new Text("Matched\t" + year), new Text(diffKey[0]));
			}
			if (diffKey[1].equals("negative")) {
				context.write(new Text("Matched\t" + year), new Text(diffKey[1]));
			}
			if (diffKey[1].equals("neutral")) {
				context.write(new Text("Matched\t" + year), new Text(diffKey[0]));
			}
		} catch (ArrayIndexOutOfBoundsException ex) {
			System.out.println("OUt of Bounds");
		}
	}
}
