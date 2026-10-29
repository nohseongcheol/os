// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class Тоологч_утга {
    int 수;
    synchronized void 더하기() { int 앞 = 수; Thread.yield(); 수 = 앞 + 1; }
}
class даалгавар_үйлдэл implements Runnable {
    Тоологч_утга Тоологч_Толь_лавлах; даалгавар_үйлдэл(Тоологч_утга Тоологч_Толь_лавлах) { this.Тоологч_Толь_лавлах = Тоологч_Толь_лавлах; }
    public void run() { for (int i = 0; i < 20; i++) Тоологч_Толь_лавлах.더하기(); }
}
class яриа_утга extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        Тоологч_утга Тоологч_Толь_лавлах = new Тоологч_утга(); Thread 하나 = new Thread(new даалгавар_үйлдэл(Тоологч_Толь_лавлах)); Thread 둘 = new Thread(new даалгавар_үйлдэл(Тоологч_Толь_лавлах));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(Тоологч_Толь_лавлах.수); System.out.println(하나.isAlive());
        яриа_утга 셋 = new яриа_утга(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 거부"); }
        System.out.println("яриа_утга 완료");
    }
}
