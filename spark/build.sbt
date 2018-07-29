name := "spark"

version := "1.0"

scalaVersion := "2.11.1"

libraryDependencies ++= {
  Seq(
    "org.apache.spark" %% "spark-core" % "1.6.0",
    "org.apache.spark" % "spark-streaming_2.11" % "1.6.0",
    "org.apache.spark" %% "spark-streaming-kafka" % "1.6.0"
  )
}

fork in Test := true
