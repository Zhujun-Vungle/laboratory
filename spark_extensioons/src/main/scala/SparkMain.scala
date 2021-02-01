package com.hbp.pipe

import org.apache.spark.SparkConf
import org.apache.spark.sql.SparkSession

object SparkMain {
  def main(args: Array[String]): Unit = {
    import java.util.UUID
    import java.time.LocalDate
    val s3_key = args(0)
    val s3_secret = args(1)
    val start_date = args(2)
    val end_date = args(3)
    val partitions_num = args(4).toInt

    println(s"s3_key: $s3_key, s3_secret: $s3_secret, start_date: $start_date, end_date: $end_date")

    //    val stagingDir  = (dt: LocalDate) => s"s3a://vungle2-dataeng/temp/hbp_archive/$dt/${UUID.randomUUID}/"

    var startDate = LocalDate.parse(start_date)
    val endDate = LocalDate.parse(end_date)
    val src = "s3a://vungle2-dataeng/archive/hbp_transactions_archive/"
    val dst = "s3a://vungle2-dataeng/archive_stage/temp/hbp_transactions_archive_new/"
    val temp_view = "archived_hbp"
    lazy val sparkConf = new SparkConf()

    //   .foreach(x => sparkConf.set(x._1,x._2))
    sparkConf.setAll(Map(
      "spark.signal_fx.secret.api_key" -> "",

      "spark.app.is_backfill" -> "false",
      "spark.app.backfill.hours" -> "0",

      "spark.app.batch_jobs.db.secret.password" -> "",

      "spark.app.hbp.archive.numPartitionsForWrite" -> "400",
      "spark.app.hbp.archive.tablePrefix" -> "",

      "spark.speculation" -> "false",
      "spark.hadoop.fs.s3a.fast.upload" -> "true",
      // FYI https://issues.apache.org/jira/browse/SPARK-10063
      "spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version" -> "2",
      "spark.hadoop.fs.s3a.impl" -> "org.apache.hadoop.fs.s3a.S3AFileSystem",
      "spark.hadoop.fs.s3a.fast.upload" -> "true",
      "spark.hadoop.fs.s3a.fast.upload.active.blocks" -> "1",
      "spark.hadoop.fs.s3a.buffer.dir" -> "/mnt",
      "spark.hadoop.fs.s3a.fast.upload.buffer" -> "bytebuffer",
      "spark.hadoop.fs.s3a.access.key" -> s3_key,
      "spark.hadoop.fs.s3a.secret.key" -> s3_secret
    ))

    val spark = SparkSession.builder.config(sparkConf).getOrCreate()
    while (startDate != endDate) {
      println(s"Processing last_updated_at date $startDate")
      List("hr=00", "hr=01", "hr=02", "hr=03", "hr=04", "hr=05", "hr=06", "hr=07", "hr=08", "hr=09", "hr=10", "hr=11", "hr=12", "hr=13", "hr=14", "hr=15", "hr=16", "hr=17", "hr=18", "hr=19", "hr=20", "hr=21", "hr=22", "hr=23").foreach{
        hr =>
          spark.read.parquet(s"$src/dt=$startDate/$hr/*").createOrReplaceTempView(temp_view)
          spark.sql(
            s"""
            SELECT date_format(timestamp_at_auction, "y-MM-dd") AS dt,
                   date_format(timestamp_at_auction, "HH")      AS hr,
                   *
              FROM $temp_view
          """)
            .coalesce(partitions_num)
            .write
            .format("parquet")
            .mode("append")
            .partitionBy("dt", "hr")
            .save(dst)

          println(s"Saved data from $src/dt=$startDate/$hr to $dst")
      }

      startDate = startDate.plusDays(1)
    }
  }
}
