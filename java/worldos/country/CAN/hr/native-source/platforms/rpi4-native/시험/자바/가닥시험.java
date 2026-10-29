// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class brojač_posjeta_VALUE {
    int 수;
    synchronized void 더하기() { int prednja_VALUE = 수; Thread.yield(); 수 = prednja_VALUE + 1; }
}
class obaveza_akcija implements Runnable {
    brojač_posjeta_VALUE brojač_posjeta_Reference; obaveza_akcija(brojač_posjeta_VALUE brojač_posjeta_Reference) { this.brojač_posjeta_Reference = brojač_posjeta_Reference; }
    public void run() { for (int i = 0; i < 20; i++) brojač_posjeta_Reference.더하기(); }
}
class nit_VALUE extends Thread { public void run() { synchronized (가닥시험.zaključati_VALUE) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object zaključati_VALUE = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        brojač_posjeta_VALUE brojač_posjeta_Reference = new brojač_posjeta_VALUE(); Thread 하나 = new Thread(new obaveza_akcija(brojač_posjeta_Reference)); Thread 둘 = new Thread(new obaveza_akcija(brojač_posjeta_Reference));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(brojač_posjeta_Reference.수); System.out.println(하나.isAlive());
        nit_VALUE 셋 = new nit_VALUE(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 odbiti_VALUE"); }
        System.out.println("nit_VALUE 완료");
    }
}
