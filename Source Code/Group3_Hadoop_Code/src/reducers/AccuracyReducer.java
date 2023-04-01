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
		int posNeg = 0;
		int posNeu = 0;
		int negPos = 0;
		int negNeu = 0;
		int neuPos = 0;
		int neuNeg = 0;
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
					if(modelled.equals("negative")) {
						posNeg ++;
					} else {
						posNeu ++;
					}
				} else if (actual.equals("negative")) {
					if(modelled.equals("positive")) {
						negPos ++;
					} else {
						negNeu ++;
					}
				} else {
					if(modelled.equals("positive")) {
						neuPos ++;
					} else {
						neuNeg ++;
					}
				}
			}
			total ++;
		}
		// formula and writing to context the values from the two category
		int correct = truePositive + trueNegative + trueNeutral;
		double accuracy = (double) correct/total * 100.0;
		context.write(key, new Text("Positive Positive: " + truePositive));
		context.write(key, new Text("Negative Negative: " + trueNegative));
		context.write(key, new Text("Neutral Neutral: " + trueNeutral));
		context.write(key, new Text("Positive Negative: " + posNeg));
		context.write(key, new Text("Negative Positive: " + negPos));
		context.write(key, new Text("Neutral Positive: " + neuPos));
		context.write(key, new Text("Positive Neutral: " + posNeu));
		context.write(key, new Text("Negative Neutral: " + negNeu));
		context.write(key, new Text("Neutral Negative: " + neuNeg));
		context.write(key, new Text("Total: " + total));
		context.write(key, new Text("Accuracy: " + accuracy));
	}
}
