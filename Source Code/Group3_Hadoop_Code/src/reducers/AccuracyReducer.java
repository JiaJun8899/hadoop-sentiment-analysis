package reducers;

import java.io.IOException;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class AccuracyReducer extends Reducer<Text, Text, Text, Text>{

	@Override
	protected void reduce(Text key, Iterable<Text> values, Reducer<Text, Text, Text, Text>.Context context) throws IOException, InterruptedException {
		// values needed for accuracy calculation
		int truePositive = 0;
		int trueNegative = 0;
		int trueNeutral = 0;
		int falsePositive = 0;
		int falseNegative = 0;
		int falseNeutral = 0;
		int total = 0;
		// loop all the values with the associated key
		for (Text senti: values) {
			String[] parts = senti.toString().split("\t");
			// get the actual rating
			String actual = parts[1];
			// get created model's rating
			String modelled = parts[2];
			// checker to see if it matches with the user's sentiment
			if (actual.equals(modelled)) {
				if(actual.equals("positive")) {
					truePositive ++;
				} else if (actual.equals("negative")) {
					trueNegative ++;
				} else {
					trueNeutral++;
				}
			} else {
				if(actual.equals("positive")) {
					falseNegative ++;
				} else if (actual.equals("negative")) {
					falsePositive ++;
				} else {
					falseNeutral++;
				}
			}
			total ++;
		}
		// formula and writing to context the values from the two category
		int correct = truePositive + trueNegative + trueNeutral;
		double accuracy = (double) correct/total * 100.0;
		context.write(key, new Text("True Positive: " + truePositive));
		context.write(key, new Text("True Negative: " + trueNegative));
		context.write(key, new Text("True Neutral: " + trueNeutral));
		context.write(key, new Text("False Positive: " + falsePositive));
		context.write(key, new Text("False Negative: " + falseNegative));
		context.write(key, new Text("False Neutral: " + falseNeutral));
		context.write(key, new Text("Total: " + total));
		context.write(key, new Text("Accuracy: " + accuracy));
	}
}
