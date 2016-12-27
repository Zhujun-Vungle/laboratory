import org.apache.spark.rdd.RDD
import org.apache.spark.streaming.dstream.InputDStream
import org.apache.spark.streaming.{StreamingContext, Time}

/**
 * Created by huiqiangliu on 15/11/25.
 */
class ConstantStream(@transient ssc_ : StreamingContext, numPerBatch: Int) extends InputDStream[String](ssc_) {
  var counter: Int = 0

  override def compute(validTime: Time): Option[RDD[String]] = {
    val prefix = validTime.toString()

    val data = Range(0, numPerBatch).map(_ + counter).map(prefix + ": " + _.toString)
    counter += numPerBatch
    Some(ssc_.sparkContext.parallelize(data))
  }

  override def start(): Unit = {
    counter = 0
  }

  def stop(): Unit = {
  }
}
