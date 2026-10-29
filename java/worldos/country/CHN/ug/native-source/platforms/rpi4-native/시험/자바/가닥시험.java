// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class سانىغۇچ_قىممىتى {
    int 수;
    synchronized void 더하기() { int 앞 = 수; Thread.yield(); 수 = 앞 + 1; }
}
class ۋەزىپە_ھەرىكەت implements Runnable {
    سانىغۇچ_قىممىتى سانىغۇچ_پايدىلانما; ۋەزىپە_ھەرىكەت(سانىغۇچ_قىممىتى سانىغۇچ_پايدىلانما) { this.سانىغۇچ_پايدىلانما = سانىغۇچ_پايدىلانما; }
    public void run() { for (int i = 0; i < 20; i++) سانىغۇچ_پايدىلانما.더하기(); }
}
class ئېقىم_قىممىتى_5b72a632 extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        سانىغۇچ_قىممىتى سانىغۇچ_پايدىلانما = new سانىغۇچ_قىممىتى(); Thread 하나 = new Thread(new ۋەزىپە_ھەرىكەت(سانىغۇچ_پايدىلانما)); Thread 둘 = new Thread(new ۋەزىپە_ھەرىكەت(سانىغۇچ_پايدىلانما));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(سانىغۇچ_پايدىلانما.수); System.out.println(하나.isAlive());
        ئېقىم_قىممىتى_5b72a632 셋 = new ئېقىم_قىممىتى_5b72a632(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 거부"); }
        System.out.println("ئېقىم_قىممىتى_5b72a632 완료");
    }
}
