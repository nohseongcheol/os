// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class Zieler_VALUE {
    int 수;
    synchronized void 더하기() { int 앞 = 수; Thread.yield(); 수 = 앞 + 1; }
}
class To_do_Aktioun implements Runnable {
    Zieler_VALUE Zieler_Referenzen; To_do_Aktioun(Zieler_VALUE Zieler_Referenzen) { this.Zieler_Referenzen = Zieler_Referenzen; }
    public void run() { for (int i = 0; i < 20; i++) Zieler_Referenzen.더하기(); }
}
class Thread_VALUE extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        Zieler_VALUE Zieler_Referenzen = new Zieler_VALUE(); Thread 하나 = new Thread(new To_do_Aktioun(Zieler_Referenzen)); Thread 둘 = new Thread(new To_do_Aktioun(Zieler_Referenzen));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(Zieler_Referenzen.수); System.out.println(하나.isAlive());
        Thread_VALUE 셋 = new Thread_VALUE(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 거부"); }
        System.out.println("Thread_VALUE 완료");
    }
}
