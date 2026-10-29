// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class teller_VERDI {
    int nummer;
    synchronized void 더하기() { int frontkamera_VERDI = nummer; Thread.yield(); nummer = frontkamera_VERDI + 1; }
}
class oppgave_Gjøremål implements Runnable {
    teller_VERDI teller_referere; oppgave_Gjøremål(teller_VERDI teller_referere) { this.teller_referere = teller_referere; }
    public void run() { for (int i = 0; i < 20; i++) teller_referere.더하기(); }
}
class tråd_VERDI extends Thread { public void run() { synchronized (가닥시험.blokkere_VERDI) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object blokkere_VERDI = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        teller_VERDI teller_referere = new teller_VERDI(); Thread 하나 = new Thread(new oppgave_Gjøremål(teller_referere)); Thread 둘 = new Thread(new oppgave_Gjøremål(teller_referere));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(teller_referere.nummer); System.out.println(하나.isAlive());
        tråd_VERDI 셋 = new tråd_VERDI(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 avvise_VERDI"); }
        System.out.println("tråd_VERDI 완료");
    }
}
