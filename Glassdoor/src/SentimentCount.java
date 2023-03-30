import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.chain.ChainMapper;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import java.net.URI;

public class SentimentCount {
	public static void main(String[] args) throws Exception {
		Configuration conf = new Configuration();
		Job job = Job.getInstance(conf, "SentimentCount");
		job.setJarByClass(SentimentCount.class);

		Path inPath = new Path("hdfs://localhost:9000/user/jiajun/project/input/");
		Path outPath = new Path("hdfs://localhost:9000/user/jiajun/project/output");
		outPath.getFileSystem(conf).delete(outPath, true);

		// Put this file to distributed cache so we can use it to join
		job.addCacheFile(new URI("hdfs://localhost:9000/user/jiajun/project/Utils/AFINN.tsv"));
		job.addCacheFile(new URI("hdfs://localhost:9000/user/jiajun/project/Utils/stopwords.txt"));
		
		Configuration validationConf = new Configuration(false);
		ChainMapper.addMapper(job, SentimentValidationMapper.class, LongWritable.class, Text.class, LongWritable.class,Text.class, validationConf);

		Configuration ansConf = new Configuration(false);
		ChainMapper.addMapper(job, SentimentMapper.class, LongWritable.class, Text.class, Text.class, IntWritable.class,ansConf);

		job.setMapperClass(ChainMapper.class);

		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(Text.class);

		FileInputFormat.addInputPath(job, inPath);
		FileOutputFormat.setOutputPath(job, outPath);
		System.exit(job.waitForCompletion(true) ? 0 : 1);
	}
}