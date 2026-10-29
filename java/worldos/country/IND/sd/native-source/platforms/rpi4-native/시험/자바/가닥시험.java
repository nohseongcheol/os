// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class ڳڻندڙ_قدر {
    int 수;
    synchronized void 더하기() { int 앞 = 수; Thread.yield(); 수 = 앞 + 1; }
}
class ٽاسڪ_عمل implements Runnable {
    ڳڻندڙ_قدر ڳڻندڙ_حوالو; ٽاسڪ_عمل(ڳڻندڙ_قدر ڳڻندڙ_حوالو) { this.ڳڻندڙ_حوالو = ڳڻندڙ_حوالو; }
    public void run() { for (int i = 0; i < 20; i++) ڳڻندڙ_حوالو.더하기(); }
}
class لڙي_قدر extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        ڳڻندڙ_قدر ڳڻندڙ_حوالو = new ڳڻندڙ_قدر(); Thread 하나 = new Thread(new ٽاسڪ_عمل(ڳڻندڙ_حوالو)); Thread 둘 = new Thread(new ٽاسڪ_عمل(ڳڻندڙ_حوالو));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(ڳڻندڙ_حوالو.수); System.out.println(하나.isAlive());
        لڙي_قدر 셋 = new لڙي_قدر(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 거부"); }
        System.out.println("لڙي_قدر 완료");
    }
}
