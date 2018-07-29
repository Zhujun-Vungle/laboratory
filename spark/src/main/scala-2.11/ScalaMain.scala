import scala.concurrent.Future

object ScalaMain {
  def main(args: Array[String]): Unit = {
    var totalA = "hello"
    val text = Future {
      "na" * 16 + "BATMAN!!!"
    }
    text onSuccess {
      case txt => totalA += txt.count(_ == 'a')
    }
    text onSuccess {
      case txt => totalA += txt.count(_ == 'A')
    }

    println(totalA)
  }
}
