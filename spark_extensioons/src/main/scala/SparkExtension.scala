import org.apache.spark.sql.catalyst.{FunctionIdentifier, TableIdentifier}
import org.apache.spark.sql.catalyst.expressions.Expression
import org.apache.spark.sql.catalyst.parser.{CatalystSqlParser, ParserInterface}
import org.apache.spark.sql.catalyst.plans.logical.LogicalPlan
import org.apache.spark.sql.catalyst.rules.Rule
import org.apache.spark.sql.types.{DataType, StructType}
import org.apache.spark.sql.{SparkSession, SparkSessionExtensions}
import org.apache.spark.{SparkConf, SparkContext}

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
    println(s.sessionState.sqlParser)
    s.stop()
  }
}
