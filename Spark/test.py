# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


import sys
from pyspark.streaming.kafka import KafkaUtils, TopicAndPartition
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import Row, SparkSession


#def getSparkSessionInstance(sparkConf):
#    if ('sparkSessionSingletonInstance' not in globals()):
#        globals()['sparkSessionSingletonInstance'] = SparkSession\
#            .builder\
#            .config(conf=sparkConf)\
#            .getOrCreate()
#    return globals()['sparkSessionSingletonInstance']

def process(time, rdd):
    """
    This function converts the RDD format to a dataframe
    """
    print("========= %s =========" % str(time))

            # Get the singleton instance of SparkSession
    spark = getSparkSessionInstance(rdd.context.getConf())

            # Convert RDD[String] to RDD[Row] to DataFrame
    rowRdd = rdd.map(lambda w: Row(word=w))
    wordsDataFrame = spark.createDataFrame(rowRdd)

            # Creates a temporary view using the DataFrame.
    wordsDataFrame.createOrReplaceTempView("words")

            # Do word count on table using SQL and print it
    wordCountsDataFrame = \
        spark.sql("select word, count(*) as total from words group by word")
    #wordCountsDataFrame

# Create a socket stream on target ip:port and count the
# words in input stream of \n delimited text (eg. generated by 'nc')
#lines = ssc.socketTextStream(host, int(port))
#words = filteredStream.flatMap(lambda line: line.split(" "))

def main():
    """
    Apply ETL on Spark Stream
    """
    batch_duration = 5
    spark_session = SparkSession.builder.appName("stocks_monitoring").getOrCreate()
    sc = spark_session.sparkContext
    sc.setLogLevel("ERROR")
    ssc = StreamingContext(sc, batch_duration)
    #sc.setCheckpointDir("hdfs://master:9000/RddCheckPoint")
    #ssc.checkpoint(checkpointDirectory)  a# set checkpoint directory
    #context = StreamingContext.getOrCreate(checkpointDirectory, functionToCreateContext)
    topic = 'rawDBGData'
    #partition = 0
    #start = 0
    #topicpartition = TopicAndPartition(topic, partition)
    #fromoffset = {topicpartition: int(start)}
    #parse the row into separate components

    #kafkaStream = KafkaUtils.createDirectStream(ssc,
    #                ['rawDBGData'], {'metadata.broker.list':
    #                '10.0.0.11:9092, 10.0.0.9:9092, 10.0.0.4:9092'}, fromOffsets = fromoffset)
    kafka_ips = '10.0.0.11:9092, 10.0.0.9:9092, 10.0.0.6:9092'

    kafkaStream = KafkaUtils.createDirectStream(ssc,
                    ['rawDBGData'], {'metadata.broker.list':
                    kafka_ips})

    #parse the row into separate components
    kafkaStream = kafkaStream.window(5)
    filteredStream = kafkaStream.flatMap(lambda line: line[1].split("^")).pprint()

        # Convert RDDs of the words DStream to DataFrame and run SQL query

    # Create a socket stream on target ip:port and count the
    # words in input stream of \n delimited text (eg. generated by 'nc')
    #lines = ssc.socketTextStream(host, int(port))
    #words = filteredStream.flatMap(lambda line: line.split(" "))

    #filteredStream.foreachRDD(process)

    ssc.start()
    ssc.awaitTermination()
    return

if __name__ == "__main__":
    main()
