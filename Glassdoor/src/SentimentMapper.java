import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.Hashtable;

public class SentimentMapper extends Mapper<LongWritable, Text, Text, IntWritable> {
	Hashtable<String, Integer> wordTable = new Hashtable<>();

	@Override
	protected void setup(Mapper<LongWritable, Text, Text, IntWritable>.Context context) throws IOException, InterruptedException {
		BufferedReader br = new BufferedReader(new FileReader("AFINN.tsv"));
		String line = null;

		while (true) {
			line = br.readLine();
			if (line != null) {
				String parts[] = line.split("\t");
				if (parts.length != 2) {
					System.out.println("Invalid line format: " + line);
				} else {
					String word = parts[0];
					String scoreStr = parts[1];
					try {
						int score = Integer.parseInt(scoreStr);
						wordTable.put(word, score);
					} catch (NumberFormatException e) {
						System.out.println("Invalid score format: " + scoreStr);
					}
				}
			} else {
				break; // finished reading
			}
		}

		br.close();
	}

	@Override
	protected void map(LongWritable key, Text value, Mapper<LongWritable, Text, Text, IntWritable>.Context context) throws IOException, InterruptedException {
		String[] parts = value.toString().split(",");
		String pros = parts[3];
		String cons = parts[4];
		Integer intVal = 0;
		String output;
		if (pros != null) {
			String[] words = pros.split("\\s+");
			String[] tokenCons = cons.split("\\s+");
			// Loop through the words in the array
			for (String word : words) {
				// Check if the word is in the hashtable
				if (wordTable.containsKey(word)) {
					// If the value associated with the word is positive, write the word and its
					// value to the context
					intVal += wordTable.get(word);
				}
			}
			for (String con : tokenCons) {
				if (wordTable.containsKey(con)) {
					intVal += wordTable.get(con);
				}
			}
			context.write(value, new IntWritable(intVal));
		}
	}

}