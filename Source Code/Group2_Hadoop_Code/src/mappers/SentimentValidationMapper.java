package mappers;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class SentimentValidationMapper extends Mapper<LongWritable, Text, LongWritable, Text> {
	List<String> stopWords = new ArrayList<>();
	Map<String, String> lemmingMap = new HashMap<>();

	@Override
	protected void setup(Mapper<LongWritable, Text, LongWritable, Text>.Context context)
			throws IOException, InterruptedException {
		BufferedReader stopWordBR = new BufferedReader(new FileReader("stopwords.txt"));
		String line = null;
		while (true) {
			line = stopWordBR.readLine();
			if (line != null) {
				stopWords.add(line.trim());
			} else {
				break; // finished reading
			}
		}
		stopWordBR.close();
		BufferedReader lemmBR = new BufferedReader(new FileReader("lemm.tsv"));
		while (true) {
			line = lemmBR.readLine();
			if (line != null) {
				String[] parts = line.split("\t");
				if (parts.length == 2) {
					lemmingMap.put(parts[1], parts[0]);
				}
			} else {
				break; // finished reading
			}
		}
		lemmBR.close();
	}

	@Override
	protected void map(LongWritable key, Text value, Mapper<LongWritable, Text, LongWritable, Text>.Context context)
			throws IOException, InterruptedException {
		String rowValue = value.toString();
		rowValue = cleanData(rowValue);
		if (isValid(rowValue)) {
			context.write(key, new Text(rowValue));
		}
	}

	private boolean isValid(String line) {
		String[] parts = line.split(",");
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
			if (i == 2) {
				continue;
			}
			line[i] = line[i].replaceAll("[^a-zA-Z0-9\\s]", "");
			line[i] = line[i].toLowerCase();
			line[i] = line[i].trim();
			line[i] = removeStopWords(line[i]);
			line[i] = lemmString(line[i]);
		}
		String output = makeString(line,",");
		return output;
	}

	private String makeString(String[] parts, String delimiter) {
		StringBuilder sb = new StringBuilder();
		for (int i = 0; i < parts.length; i++) {
			sb.append(parts[i]);
			if (i < parts.length - 1) {
				sb.append(delimiter);
			}
		}
		return sb.toString();
	}

	private String removeStopWords(String text) {
		String[] words = text.split("\\s+");
		List<String> wordsList = new ArrayList<>(Arrays.asList(words));
		wordsList.removeAll(stopWords);
		StringBuilder sb = new StringBuilder();
		for (int i = 0; i < wordsList.size(); i++) {
			sb.append(wordsList.get(i));
			if (i < wordsList.size() - 1) {
				sb.append(" ");
			}
		}
		return makeString(wordsList.toArray(new String[0])," ");
	}
	
	private String lemmString(String text) {
		String[] tokens = text.split("\\s+");
		String lemmedWord;
		for (int i = 0; i<tokens.length;i++) {
			lemmedWord = lemmingMap.get(tokens[i]);
			if(lemmedWord != null) {
				tokens[i] = lemmedWord;
			}
		}
		return makeString(tokens, " ");
	}
}
