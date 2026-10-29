// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class tæller_VÆRDI {
    int tal;
    synchronized void 더하기() { int frontvendt_VÆRDI = tal; Thread.yield(); tal = frontvendt_VÆRDI + 1; }
}
class job_To_do implements Runnable {
    tæller_VÆRDI tæller_referere; job_To_do(tæller_VÆRDI tæller_referere) { this.tæller_referere = tæller_referere; }
    public void run() { for (int i = 0; i < 20; i++) tæller_referere.더하기(); }
}
class tråd_VÆRDI extends Thread { public void run() { synchronized (가닥시험.lås_VÆRDI) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object lås_VÆRDI = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        tæller_VÆRDI tæller_referere = new tæller_VÆRDI(); Thread 하나 = new Thread(new job_To_do(tæller_referere)); Thread 둘 = new Thread(new job_To_do(tæller_referere));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(tæller_referere.tal); System.out.println(하나.isAlive());
        tråd_VÆRDI 셋 = new tråd_VÆRDI(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 afvise_VÆRDI"); }
        System.out.println("tråd_VÆRDI 완료");
    }
}
