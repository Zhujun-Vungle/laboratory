import com.typesafe.config.{Config, ConfigFactory}
import org.apache.spark._
import org.apache.spark.rdd.RDD
import org.apache.spark.streaming._

/**
  * Created by huiqiangliu on 15/7/28.
  */

object SparkStreamTest {

  def main(args: Array[String]): Unit = {

    // Allow override with command-line option
    val configFileName = System.getProperty("config.file", "SparkTest")
    val config: Config = ConfigFactory.load(configFileName)

    val ssc = createSparkStreamingContext(config)
    setupSparkStreaming(config, ssc)

    ssc.start() // Start the computation
    ssc.awaitTermination() // Wait for the computation to terminate
  }

  def createSparkStreamingContext(config: Config): StreamingContext = {
    val configKeys = Seq(
      "spark.master",
      "spark.app.name"
    )
    val sparkConfig = configKeys.filter(key => config.hasPath(key)).foldLeft(new SparkConf(true)) {
      (sparkConfig, key) => sparkConfig.set(key, config.getString(key))
    }

    new StreamingContext(new SparkContext(sparkConfig), Seconds(config.getInt("streamBatchDuration")))
  }

  def setupSparkStreaming(config: Config, ssc: StreamingContext) {

      val stream = new ConstantStream(ssc, 8)

      var index = 0

      stream.foreachRDD { rdd =>
        try {
        index += 1
        println("increase index to " + index)
        processBatch(ssc, rdd, index)
        } catch {
          case e: Exception => println("we catch this new exception aaaaa"); println(e)
        }
      }

  }

  def processBatch(ssc: StreamingContext, rdd: RDD[String], index: Int): Unit = {
    println("begin process batch " + index)
    rdd.foreach { s =>
      println(index.toString + " = " + s)
    }
//    if (index % 2 == 0) {
////      throw new Exception(s"Fatal error $index")
//    }
    /*
    println("end process batch " + index)
    if (index >= 2) {
      println("stop sc in rdd!!!")
      ssc.sparkContext.stop()
    }
    */
  }
}
