package com.colobu.kafka

/**
  * Created by jun.zhu on 9/21/16.
  */

import java.util.Properties

import kafka.consumer.{Consumer, ConsumerConfig}
import kafka.serializer.Decoder
import kafka.utils.VerifiableProperties
import org.apache.kafka.clients.consumer.{ConsumerRecord, KafkaConsumer}
import org.apache.kafka.clients.producer.{KafkaProducer, ProducerRecord}

import scala.collection.Map
import scala.reflect._

object Consumer {
  def main(args: Array[String]): Unit = {

//        consumer

    val propsConsumer = new Properties()

    propsConsumer.put("bootstrap.servers", "localhost:9092")
    propsConsumer.put("group.id", "test")
    propsConsumer.put("enable.auto.commit", "true")
    propsConsumer.put("auto.commit.interval.ms", "1000")
    propsConsumer.put("session.timeout.ms", "30000")
    propsConsumer.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer")
    propsConsumer.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer")
    propsConsumer.put("partition.assignment.strategy", "range")
    propsConsumer.put("zookeeper.connect", "localhost:2181");
    val consumerConfig = new ConsumerConfig(propsConsumer)
    val consumer = Consumer.create(consumerConfig)
    val topicCountMap: Map[String, Int] = Map("ad-server" -> 1)

    val consumerMap = consumer.createMessageStreams(topicCountMap);
    val streams = consumerMap("ad-server");
    for (stream <- streams) {
      val it = stream.iterator()

      while (it.hasNext()) {
        val msg = new String(it.next().message());
        println(msg)
      }
    }

  }
}
