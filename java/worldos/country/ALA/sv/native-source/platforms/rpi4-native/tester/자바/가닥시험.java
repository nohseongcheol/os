// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class räknare_värde {
    int nummer;
    synchronized void 더하기() { int framåtvänd_värde = nummer; Thread.yield(); nummer = framåtvänd_värde + 1; }
}
class uppgift_Action implements Runnable {
    räknare_värde räknare_referens; uppgift_Action(räknare_värde räknare_referens) { this.räknare_referens = räknare_referens; }
    public void run() { for (int i = 0; i < 20; i++) räknare_referens.더하기(); }
}
class tråd_värde extends Thread { public void run() { synchronized (가닥시험.lås_värde) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object lås_värde = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        räknare_värde räknare_referens = new räknare_värde(); Thread 하나 = new Thread(new uppgift_Action(räknare_referens)); Thread 둘 = new Thread(new uppgift_Action(räknare_referens));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(räknare_referens.nummer); System.out.println(하나.isAlive());
        tråd_värde 셋 = new tråd_värde(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 avvisa_värde"); }
        System.out.println("tråd_värde 완료");
    }
}
