package mappers;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.Hashtable;

public class SentimentMapper extends Mapper<LongWritable, Text, Text, Text> {
	Hashtable<String, Integer> sentimentScores = new Hashtable<>();

	@Override
	protected void setup(Mapper<LongWritable, Text, Text, Text>.Context context)
			throws IOException, InterruptedException {
		BufferedReader br = new BufferedReader(new FileReader("AFINN.tsv"));
		String line = null;
		while ((line = br.readLine())!= null) {
			// Splits the AFINN into the key value pairs
			String parts[] = line.split("\t");
			
			// Ensure it has 2 parts
			if (parts.length != 2) {
				System.out.println("Invalid line format: " + line);
			} else {
				// Save the key value into a hash map
				String word = parts[0];
				String wordValue = parts[1];
				
				// Catch potential errors within the file
				try {
					int score = Integer.parseInt(wordValue);
					sentimentScores.put(word, score);
				} catch (NumberFormatException e) {
					System.out.println("Invalid score format: " + wordValue);
				}
			}
		}
		br.close();
	}

	@Override
	protected void map(LongWritable key, Text value, Mapper<LongWritable, Text, Text, Text>.Context context)
			throws IOException, InterruptedException {
		// split the row into columns and extract the pros and cons
		String[] columns = value.toString().split(",");
		String pros = columns[3];
		String cons = columns[4];
		// Calculate the sentiment value and match it to the labels
		int unmatchedSentiVal = calculateSentimentValue(pros, cons, false);
		int matchedSentiVal = calculateSentimentValue(pros, cons, true);
		String matchedLabel = getSentimentLabel(matchedSentiVal);
		String unMatchLabel = getSentimentLabel(unmatchedSentiVal);
		context.write(new Text(unMatchLabel + "\t" + matchedLabel), new Text(value.toString() + "," + unmatchedSentiVal+ "," + matchedSentiVal));
	}
	
	// calculates the sentiment values
	private int calculateSentimentValue(String pros, String cons, boolean matched) {
        int sentimentValue = 0;
        // breaks into tokens
        String[] prosToken = pros.split("\\s+");
        String[] consToken = cons.split("\\s+");
        // for loops and find a hit in the hashmap, if present, add the value
        // matched = true for only taking positive for pros and negative for cons
        for (String pro : prosToken) {
            if (sentimentScores.containsKey(pro)) {
                int score = sentimentScores.get(pro);
                if (matched && score > 0) {
                    sentimentValue += score;
                } else if (matched == false) {
                	sentimentValue += score;
                }
            }
        }
        for (String con : consToken) {
            if (sentimentScores.containsKey(con)) {
                int score = sentimentScores.get(con);
                if (matched && score < 0) {
                    sentimentValue += score;
                } else if (matched == false) {
                	sentimentValue += score;
                }
            }
        }
        
        return sentimentValue;
    }
	
	// Utility function for labeling the sentiment
	private String getSentimentLabel(int sentimentValue) {
		if (sentimentValue == 0) {
			return "neutral";
		} else if (sentimentValue < 0) {
			return "negative";
		} else {
			return "positive";
		}
	}
}