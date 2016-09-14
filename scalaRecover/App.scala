/**
  * Created by jun.zhu on 9/13/16.
  */
object App {
  def main(args: Array[String]): Unit = {
    println("1: adder")
    println(CurriedMethod.adder(1,2))
    println(CurriedMethod.add4(2))

    println("2: curried function")
    val add4 = CurriedMethod.currAdd(4)
    println(add4(2))

    println("3: multi string args")
    println(InputWays.multiAguements("lily","lucy","amy"))
  }
}
