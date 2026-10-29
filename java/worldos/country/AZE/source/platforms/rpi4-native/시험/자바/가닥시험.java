// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class sayğac_VALUE {
    int 수;
    synchronized void 더하기() { int ön_VALUE = 수; Thread.yield(); 수 = ön_VALUE + 1; }
}
class tapşırıq_aktiv implements Runnable {
    sayğac_VALUE sayğac_İstinad; tapşırıq_aktiv(sayğac_VALUE sayğac_İstinad) { this.sayğac_İstinad = sayğac_İstinad; }
    public void run() { for (int i = 0; i < 20; i++) sayğac_İstinad.더하기(); }
}
class axın_VALUE_5b72a632 extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        sayğac_VALUE sayğac_İstinad = new sayğac_VALUE(); Thread 하나 = new Thread(new tapşırıq_aktiv(sayğac_İstinad)); Thread 둘 = new Thread(new tapşırıq_aktiv(sayğac_İstinad));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(sayğac_İstinad.수); System.out.println(하나.isAlive());
        axın_VALUE_5b72a632 셋 = new axın_VALUE_5b72a632(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 거부"); }
        System.out.println("axın_VALUE_5b72a632 완료");
    }
}
