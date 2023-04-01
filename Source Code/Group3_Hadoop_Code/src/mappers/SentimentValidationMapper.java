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
		// Parse cached stopwords into Stop Words List
		BufferedReader stopWordBR = new BufferedReader(new FileReader("stopwords.txt"));
		String line = null;
		while ((line = stopWordBR.readLine()) != null) {
			stopWords.add(line.trim());
		}
		stopWordBR.close();
		
		// Parse Lemmatisation into a hashmap
		BufferedReader lemmBR = new BufferedReader(new FileReader("lemm.tsv"));
		while ((line = lemmBR.readLine()) != null) {
			String[] parts = line.split("\t");
			if (parts.length == 2) {
				lemmingMap.put(parts[1], parts[0]);
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
			// write the key and the cleaned row data for the next mapper
			context.write(key, new Text(rowValue));
		}
	}
	
	// function to check if it has 6 columns and each columns cannot be empty
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

	// Function to clean data
	private String cleanData(String inputRow) {
		String[] inputColumns = inputRow.split(",");
		for (int i = 0; i < inputColumns.length; i++) {
			// skip for rating which is a float
			if (i == 2 || i == 5) {
				continue;
			}
			inputColumns[i] = inputColumns[i].toLowerCase();
			inputColumns[i] = removeStopWords(inputColumns[i]);
			inputColumns[i] = inputColumns[i].replaceAll("[^a-zA-Z0-9\\s]", "");
			inputColumns[i] = inputColumns[i].trim();
			inputColumns[i] = lemmString(inputColumns[i]);
		}
		String cleanedRow = makeString(inputColumns,",");
		return cleanedRow;
	}

	// Utility function to concat a string array into a string
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
	
	//Function to remove stop words
	private String removeStopWords(String text) {
		String[] inputTokens = text.split("\\s+");
		List<String> tokenList = new ArrayList<>(Arrays.asList(inputTokens));
		tokenList.removeAll(stopWords);
		return makeString(tokenList.toArray(new String[0])," ");
	}
	
	//Function to lemmatization of the input
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
