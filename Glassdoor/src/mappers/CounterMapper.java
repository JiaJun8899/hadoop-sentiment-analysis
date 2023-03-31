package mappers;
import java.io.IOException;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class CounterMapper extends Mapper<Text, Text, Text, Text>{

	@Override
	protected void map(Text key, Text value, Mapper<Text, Text, Text, Text>.Context context) throws IOException, InterruptedException {
		String[] parts = value.toString().split(",");
		String[] pros = parts[3].split("\\s+");
		String[] cons = parts[4].split("\\s+");
		for (String w: pros) {
			context.write(key, new Text("pros\t" + w));
		}
		for (String w: cons) {
			context.write(key, new Text("cons\t" + w));
		}
	}
}
