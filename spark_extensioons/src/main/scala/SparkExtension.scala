import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.catalyst.parser.CatalystSqlParser
import org.apache.spark.sql.catalyst.plans.logical.LogicalPlan
import org.apache.spark.sql.catalyst.rules.Rule

// How should I modify the physical plan..
object SparkExtension extends App {
  override def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder()
      .master("local[2]")
      .appName("Jun-test")


    case class MyRule(spark: SparkSession) extends Rule[LogicalPlan] {
      override def apply(plan: LogicalPlan): LogicalPlan = plan
    }

    spark.withExtensions(_.injectParser((_, _) => CatalystSqlParser))
    val s = spark.getOrCreate()
//    s.sessionState.experimentalMethods.extraStrategies
    println(s.sessionState.sqlParser)

//    s.sqlContext.experimental.extraStrategies


    s.stop()
  }
}
