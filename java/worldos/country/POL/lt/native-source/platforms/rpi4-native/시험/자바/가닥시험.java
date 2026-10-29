// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class skaitiklis_VALUE {
    int numeris;
    synchronized void 더하기() { int priekinis_VALUE = numeris; Thread.yield(); numeris = priekinis_VALUE + 1; }
}
class užduotis_gavinys implements Runnable {
    skaitiklis_VALUE skaitiklis_nuoroda; užduotis_gavinys(skaitiklis_VALUE skaitiklis_nuoroda) { this.skaitiklis_nuoroda = skaitiklis_nuoroda; }
    public void run() { for (int i = 0; i < 20; i++) skaitiklis_nuoroda.더하기(); }
}
class gija_VALUE extends Thread { public void run() { synchronized (가닥시험.užraktas_VALUE) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object užraktas_VALUE = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        skaitiklis_VALUE skaitiklis_nuoroda = new skaitiklis_VALUE(); Thread 하나 = new Thread(new užduotis_gavinys(skaitiklis_nuoroda)); Thread 둘 = new Thread(new užduotis_gavinys(skaitiklis_nuoroda));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(skaitiklis_nuoroda.numeris); System.out.println(하나.isAlive());
        gija_VALUE 셋 = new gija_VALUE(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 atmesti_VALUE"); }
        System.out.println("gija_VALUE 완료");
    }
}
