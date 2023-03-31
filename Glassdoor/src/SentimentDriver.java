import java.net.URI;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.chain.ChainMapper;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import mappers.CounterMapper;
import mappers.JobMapper;
import mappers.SentimentMapper;
import mappers.SentimentValidationMapper;
import mappers.YearMapper;
import reducers.CounterReducer;
import reducers.JobReducer;
import reducers.YearReducer;

public class SentimentDriver {
	public static void main(String[] args) throws Exception {
		Configuration conf = new Configuration();
		Job counterJob = Job.getInstance(conf, "SentimentCount");
		counterJob.setJarByClass(SentimentDriver.class);
		counterJob.setMapperClass(ChainMapper.class);
		counterJob.setReducerClass(CounterReducer.class);

		counterJob.setOutputKeyClass(Text.class);
		counterJob.setOutputValueClass(IntWritable.class);

		Path inPath = new Path("hdfs://hadoop-master:9000/user/ict2101351/project/input/");
		Path counterOutPath = new Path("hdfs://hadoop-master:9000/user/ict2101351/project/output/counter");
		counterOutPath.getFileSystem(conf).delete(counterOutPath, true);

		// Put this file to distributed cache so we can use it to join
		counterJob.addCacheFile(new URI("hdfs://hadoop-master:9000/user/ict2101351/project/Utils/AFINN.tsv"));
		counterJob.addCacheFile(new URI("hdfs://hadoop-master:9000/user/ict2101351/project/Utils/stopwords.txt"));

		Configuration validationConf = new Configuration(false);
		ChainMapper.addMapper(counterJob, SentimentValidationMapper.class, LongWritable.class, Text.class, LongWritable.class,
				Text.class, validationConf);

		Configuration sentiConfig = new Configuration(false);
		ChainMapper.addMapper(counterJob, SentimentMapper.class, LongWritable.class, Text.class, Text.class, Text.class,
				sentiConfig);

		Configuration counterConf = new Configuration(false);
		ChainMapper.addMapper(counterJob, CounterMapper.class, Text.class, Text.class, Text.class, Text.class, counterConf);

		FileInputFormat.addInputPath(counterJob, inPath);
		FileOutputFormat.setOutputPath(counterJob, counterOutPath);
		
		Configuration conf2 = new Configuration();
		Job yearJob = Job.getInstance(conf2, "SentimentCount");
		yearJob.setJarByClass(SentimentDriver.class);
		yearJob.setMapperClass(ChainMapper.class);
		yearJob.setReducerClass(YearReducer.class);

		yearJob.setOutputKeyClass(Text.class);
		yearJob.setOutputValueClass(IntWritable.class);

		Path yearOutPath = new Path("hdfs://hadoop-master:9000/user/ict2101351/project/output/year");
		yearOutPath.getFileSystem(conf2).delete(yearOutPath, true);

		// Put this file to distributed cache so we can use it to join
		yearJob.addCacheFile(new URI("hdfs://hadoop-master:9000/user/ict2101351/project/Utils/AFINN.tsv"));
		yearJob.addCacheFile(new URI("hdfs://hadoop-master:9000/user/ict2101351/project/Utils/stopwords.txt"));

		ChainMapper.addMapper(yearJob, SentimentValidationMapper.class, LongWritable.class, Text.class, LongWritable.class,
				Text.class, validationConf);
		ChainMapper.addMapper(yearJob, SentimentMapper.class, LongWritable.class, Text.class, Text.class, Text.class,
				sentiConfig);
		Configuration yearConf = new Configuration(false);
		ChainMapper.addMapper(yearJob, YearMapper.class, Text.class, Text.class, Text.class, Text.class, yearConf);

		FileInputFormat.addInputPath(yearJob, inPath);
		FileOutputFormat.setOutputPath(yearJob, yearOutPath);
		
		Configuration conf3 = new Configuration();
		Job jobJob = Job.getInstance(conf3, "SentimentCount");
		jobJob.setJarByClass(SentimentDriver.class);
		jobJob.setMapperClass(ChainMapper.class);
		jobJob.setReducerClass(JobReducer.class);

		jobJob.setOutputKeyClass(Text.class);
		jobJob.setOutputValueClass(IntWritable.class);

		Path jobOutPath = new Path("hdfs://hadoop-master:9000/user/ict2101351/project/output/job");
		jobOutPath.getFileSystem(conf3).delete(jobOutPath, true);

		// Put this file to distributed cache so we can use it to join
		jobJob.addCacheFile(new URI("hdfs://hadoop-master:9000/user/ict2101351/project/Utils/AFINN.tsv"));
		jobJob.addCacheFile(new URI("hdfs://hadoop-master:9000/user/ict2101351/project/Utils/stopwords.txt"));

		ChainMapper.addMapper(jobJob, SentimentValidationMapper.class, LongWritable.class, Text.class, LongWritable.class,
				Text.class, validationConf);
		ChainMapper.addMapper(jobJob, SentimentMapper.class, LongWritable.class, Text.class, Text.class, Text.class,
				sentiConfig);
		Configuration jobConf = new Configuration(false);
		ChainMapper.addMapper(jobJob, JobMapper.class, Text.class, Text.class, Text.class, Text.class, jobConf);

		FileInputFormat.addInputPath(jobJob, inPath);
		FileOutputFormat.setOutputPath(jobJob, jobOutPath);

		boolean job1Success = counterJob.waitForCompletion(true);
        if (job1Success) {
        	System.out.println("Word Counter Job Done");
            boolean job2Success = yearJob.waitForCompletion(true);
            if(job2Success){
            	System.out.println("Year Analysis Done");
				boolean job3Success = jobJob.waitForCompletion(true);
				System.out.println("Job Analysis Done");
				System.exit(job3Success ? 0 : 1);
			}
        } else {
            System.exit(1);
        }
	}
}