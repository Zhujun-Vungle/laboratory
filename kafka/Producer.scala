package com.colobu.kafka

import java.util.Properties

import org.apache.kafka.clients.producer.{KafkaProducer, ProducerRecord}

/**
  * Created by jun.zhu on 9/22/16.
  */
object Producer {
  def main(args: Array[String]): Unit = {
    val props = new Properties()
    props.put("bootstrap.servers", "localhost:9092")
    props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer")
    props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer")

    val producer = new KafkaProducer[String, String](props)
    val TOPIC = "ad-server"
    val record1 = new ProducerRecord(TOPIC, "key", "hello aaa")
    val record2 = new ProducerRecord(TOPIC, "key", "hello zzz")

    producer send record1
    producer send record2

    producer close()
  }
}
