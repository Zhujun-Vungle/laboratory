import org.apache.spark.sql.SparkSession


object SparkSqlExperimental {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder()
      .master("local[2]")
      .appName("Jun-test").getOrCreate()


    // What is the difference
    spark.experimental.extraStrategies

    spark.stop()
  }
}
