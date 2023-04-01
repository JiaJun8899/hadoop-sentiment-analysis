package reducers;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class CounterReducer extends Reducer<Text, Text, Text, Text>{
	
	@Override
	protected void reduce(Text key, Iterable<Text> values, Reducer<Text, Text, Text, Text>.Context context) throws IOException, InterruptedException {
		Map<String, Integer> proMap = new HashMap<>();
		Map<String, Integer> conMap = new HashMap<>();
		for (Text value : values) {
			String[] parts = value.toString().split("\t");
			if (parts[0].equals("pros")) {
				Integer count = proMap.get(parts[1]);
				if (count == null) {
					proMap.put(parts[1], 1);
				} else {
					proMap.put(parts[1], count + 1);
				}
			} else if (parts[0].equals("cons")) {
				Integer count = proMap.get(parts[1]);
				if (count == null) {
					conMap.put(parts[1], 1);
				} else {
					conMap.put(parts[1], count + 1);
				}
			}
		}
		for (Map.Entry<String, Integer> entry: proMap.entrySet()) {
			context.write(new Text(key.toString() + "-pros"), new Text(entry.getKey() + " " + entry.getValue()));
		}
		for (Map.Entry<String, Integer> entry: conMap.entrySet()) {
			context.write(new Text(key.toString() + "-cons"), new Text(entry.getKey() + " " + entry.getValue()));
		}
	}
}
