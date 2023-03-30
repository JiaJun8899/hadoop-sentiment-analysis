import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class SentimentValidationMapper extends Mapper<LongWritable, Text, LongWritable, Text> {
	List<String> stopWords;

	@Override
	protected void setup(Mapper<LongWritable, Text, LongWritable, Text>.Context context)
			throws IOException, InterruptedException {
		List<String> words = new ArrayList<>();
		BufferedReader br = new BufferedReader(new FileReader("stopwords.txt"));
		String line = null;
		while (true) {
			line = br.readLine();
			if (line != null) {
				words.add(line.trim());
			} else {
				break; // finished reading
			}
		}
		br.close();
		stopWords = words;
	}

	@Override
	protected void map(LongWritable key, Text value, Mapper<LongWritable, Text, LongWritable, Text>.Context context)
			throws IOException, InterruptedException {
		String rowValue = value.toString();
		if (isValid(rowValue)) {
			rowValue = cleanData(rowValue);
			context.write(key, new Text(rowValue));
		}
	}

	private boolean isValid(String line) {
		String[] parts = cleanData(line).split(",");
		if (parts.length == 6) {
			for (String part : parts) {
				if (part.isEmpty()) {
					return false;
				}
			}
			return true;
		} else {
			return false;
		}
	}

	private String cleanData(String str) {
		String[] line = str.split(",");
		for (int i = 0; i < line.length; i++) {
			line[i] = line[i].replaceAll("[^a-zA-Z\\s]", "");
			line[i] = removeStopWords(line[i]);
			line[i] = line[i].toLowerCase();
			line[i] = line[i].trim();
		}
		String output = makeString(line);
		return output;
	}

	private String makeString(String[] parts) {
		StringBuilder sb = new StringBuilder();
		for (int i = 0; i < parts.length; i++) {

			sb.append(parts[i]);
			if (i < parts.length - 1) {
				sb.append(",");
			}
		}
		System.out.println(sb.toString());
		return sb.toString();
	}

	private String removeStopWords(String text) {
		String[] words = text.split("\\s+");
		List<String> wordsList = new ArrayList<>(Arrays.asList(words));
		wordsList.removeAll(stopWords);
		return String.join(" ", wordsList);
	}
}
