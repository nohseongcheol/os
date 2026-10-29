// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class teller_WAARDE {
    int nummer;
    synchronized void 더하기() { int voorkant_WAARDE = nummer; Thread.yield(); nummer = voorkant_WAARDE + 1; }
}
class taak_Actie implements Runnable {
    teller_WAARDE teller_verwijzen; taak_Actie(teller_WAARDE teller_verwijzen) { this.teller_verwijzen = teller_verwijzen; }
    public void run() { for (int i = 0; i < 20; i++) teller_verwijzen.더하기(); }
}
class thread_WAARDE extends Thread { public void run() { synchronized (가닥시험.vergrendelen_WAARDE) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object vergrendelen_WAARDE = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        teller_WAARDE teller_verwijzen = new teller_WAARDE(); Thread 하나 = new Thread(new taak_Actie(teller_verwijzen)); Thread 둘 = new Thread(new taak_Actie(teller_verwijzen));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(teller_verwijzen.nummer); System.out.println(하나.isAlive());
        thread_WAARDE 셋 = new thread_WAARDE(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 weigeren_WAARDE"); }
        System.out.println("thread_WAARDE 완료");
    }
}
