import org.apache.spark.sql.SparkSession

object SparkJDBCRedshift {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder()
      .master("local[2]")
      .appName("Jun-test").getOrCreate()

    //https://spark.apache.org/docs/latest/sql-data-sources-jdbc.html
    // Need to add --driver-class-path com.amazon.redshift.jdbc42.Driver to applications
    // Could set that in intellj edit configuration
    val sql =
      s"""
          CREATE TEMPORARY VIEW jdbcTable
              USING org.apache.spark.sql.jdbc
              OPTIONS (
                  url "jdbc:postgresql://dataeng-stage.c3livwoqjkry.us-east-1.redshift.amazonaws.com:5439/stage",
                  dbtable "idsp_transactions",
                  user 'root',
                  password '*************'
              )
         """

    spark.sql(sql)
    spark.sql("Show tables").show(110, false)

    // It shows select event_id from idsp_transactions in cheezit, the API did not do the limit push down
//    spark.sql("select event_id from jdbctable limit 1").show(10, truncate = false)

////////////////////////////////////////////////////////////////////////////////////////////////////////////

    spark.sql("explain extended select event_id from jdbctable limit 1").show(10, truncate = false)
//    +----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
//    |plan                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
//    +----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
//    |== Parsed Logical Plan ==
//    'GlobalLimit 1
//    +- 'LocalLimit 1
//    +- 'Project ['event_id]
//    +- 'UnresolvedRelation `jdbctable`
//
//    == Analyzed Logical Plan ==
//    event_id: string
//    GlobalLimit 1
//    +- LocalLimit 1
//    +- Project [event_id#0]
//    +- SubqueryAlias `jdbctable`
//    +- Relation[event_id#0,created_at#1,last_updated_at#2,timestamp_at_delivery#3,timestamp_at_impression#4,ip_address_at_delivery#5,ip_address_at_impression#6,dev_id_at_delivery#7,dev_id_at_impression#8,dev_make#9,dev_model#10,dev_platform#11,dev_platform_version#12,dev_timezone_at_delivery#13,dev_timezone_at_impression#14,dev_language_at_delivery#15,dev_language_at_impression#16,dev_connection_at_delivery#17,dev_connection_at_impression#18,dev_network_operator_at_delivery#19,dev_network_operator_at_impression#20,dev_sound_enabled_at_delivery#21,dev_sound_enabled_at_impression#22,dev_sound_volume_at_delivery#23,... 118 more fields] JDBCRelation(idsp_transactions) [numPartitions=1]
//
//    == Optimized Logical Plan ==
//    GlobalLimit 1
//    +- LocalLimit 1
//    +- Project [event_id#0]
//    +- Relation[event_id#0,created_at#1,last_updated_at#2,timestamp_at_delivery#3,timestamp_at_impression#4,ip_address_at_delivery#5,ip_address_at_impression#6,dev_id_at_delivery#7,dev_id_at_impression#8,dev_make#9,dev_model#10,dev_platform#11,dev_platform_version#12,dev_timezone_at_delivery#13,dev_timezone_at_impression#14,dev_language_at_delivery#15,dev_language_at_impression#16,dev_connection_at_delivery#17,dev_connection_at_impression#18,dev_network_operator_at_delivery#19,dev_network_operator_at_impression#20,dev_sound_enabled_at_delivery#21,dev_sound_enabled_at_impression#22,dev_sound_volume_at_delivery#23,... 118 more fields] JDBCRelation(idsp_transactions) [numPartitions=1]
//
//    == Physical Plan ==
//      CollectLimit 1
//    +- *(1) Scan JDBCRelation(idsp_transactions) [numPartitions=1] [event_id#0] PushedFilters: [], ReadSchema: struct<event_id:string>|
//      +----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
     spark.stop()
  }
}
