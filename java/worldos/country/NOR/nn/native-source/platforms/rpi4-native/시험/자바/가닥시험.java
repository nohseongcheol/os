// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class teljar_VALUE {
    int 수;
    synchronized void 더하기() { int 앞 = 수; Thread.yield(); 수 = 앞 + 1; }
}
class oppgåve_handling implements Runnable {
    teljar_VALUE teljar_Oppslagsverk; oppgåve_handling(teljar_VALUE teljar_Oppslagsverk) { this.teljar_Oppslagsverk = teljar_Oppslagsverk; }
    public void run() { for (int i = 0; i < 20; i++) teljar_Oppslagsverk.더하기(); }
}
class tråd_VALUE extends Thread { public void run() { synchronized (가닥시험.blokkere_VALUE) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object blokkere_VALUE = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        teljar_VALUE teljar_Oppslagsverk = new teljar_VALUE(); Thread 하나 = new Thread(new oppgåve_handling(teljar_Oppslagsverk)); Thread 둘 = new Thread(new oppgåve_handling(teljar_Oppslagsverk));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(teljar_Oppslagsverk.수); System.out.println(하나.isAlive());
        tråd_VALUE 셋 = new tråd_VALUE(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 avvise_VALUE"); }
        System.out.println("tråd_VALUE 완료");
    }
}
