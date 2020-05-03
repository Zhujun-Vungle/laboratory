name := "spark"

version := "1.0"

scalaVersion := "2.12.10"
sparkVersion := "2.4.4"

resolvers += "Typesafe Repository" at "http://repo.typesafe.com/typesafe/releases/"

libraryDependencies ++= {
  Seq(
    // Structed streaming
    "org.apache.spark" %% "spark-sql-kafka-0-10" % sparkVersion exclude("net.jpountz.lz4", "lz4"),
    "org.apache.spark" %% "spark-sql" % sparkVersion % "provided",

    // typesafe
    "com.typesafe" % "config" % "1.3.2",

    // Zookeeper
    "com.twitter" %% "util-zk" % "6.27.0",

    // for s3a to work
    "com.amazonaws" % "aws-java-sdk" % "1.7.4" excludeAll(
      ExclusionRule("com.fasterxml.jackson.core", "jackson-annotations"),
      ExclusionRule("com.fasterxml.jackson.core", "jackson-core"),
      ExclusionRule("com.fasterxml.jackson.core", "jackson-databind")
    ),

    "org.apache.hadoop" % "hadoop-aws" % "2.7.2" excludeAll(
      ExclusionRule("com.amazonaws", "aws-java-sdk"),
      ExclusionRule("commons-beanutils"),
      ExclusionRule("com.fasterxml.jackson.core", "jackson-annotations"),
      ExclusionRule("com.fasterxml.jackson.core", "jackson-core"),
      ExclusionRule("com.fasterxml.jackson.core", "jackson-databind")
    ),
  )
}


assemblyMergeStrategy in assembly := {
  case m if m.toLowerCase.endsWith("manifest.mf") => MergeStrategy.discard
  case m if m.toLowerCase.matches("meta-inf.*\\.sf$") => MergeStrategy.discard
  case "log4j.properties" => MergeStrategy.discard
  case m if m.toLowerCase.startsWith("meta-inf/services/") =>
    MergeStrategy.filterDistinctLines
  case "reference.conf" => MergeStrategy.concat
  case _ => MergeStrategy.first
}

initialize := {
  initialize.value
  if (sys.props("java.specification.version") != "1.8") {
    sys.error("Java 8 is required for this project.")
  }
}

javacOptions ++= Seq("-source",
  "1.8",
  "-target",
  "1.8",
  "-Xlint")

javaOptions ++= Seq("-Xms512M",
  "-Xmx2048M",
  "-XX:MaxPermSize=2048M",
  "-XX:+CMSClassUnloadingEnabled")

test in assembly := {}

parallelExecution in Test := false

fork in Test := true
