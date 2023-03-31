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
		try {
			if (Float.parseFloat(parts[6]) > 0.0) {
				context.write(new Text(dateStr[2]), new Text("year\tpositive"));
			}
			if (Float.parseFloat(parts[6]) < 0.0) {
				context.write(new Text(dateStr[2]), new Text("year\tnegative"));
			}
			if (Float.parseFloat(parts[6]) == 0.0) {
				context.write(new Text(dateStr[2]), new Text("year\tneutral"));
			}
		} catch (NumberFormatException | ArrayIndexOutOfBoundsException ex) {
			System.out.println("Write fail");
		}
	}
}
