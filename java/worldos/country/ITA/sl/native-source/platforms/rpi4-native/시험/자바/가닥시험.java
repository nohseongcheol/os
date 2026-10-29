// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class števec_VALUE {
    int 수;
    synchronized void 더하기() { int sprednja_VALUE = 수; Thread.yield(); 수 = sprednja_VALUE + 1; }
}
class opravek_akcija implements Runnable {
    števec_VALUE števec_Gradiva; opravek_akcija(števec_VALUE števec_Gradiva) { this.števec_Gradiva = števec_Gradiva; }
    public void run() { for (int i = 0; i < 20; i++) števec_Gradiva.더하기(); }
}
class nit_VALUE extends Thread { public void run() { synchronized (가닥시험.zaklepanje_VALUE) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object zaklepanje_VALUE = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        števec_VALUE števec_Gradiva = new števec_VALUE(); Thread 하나 = new Thread(new opravek_akcija(števec_Gradiva)); Thread 둘 = new Thread(new opravek_akcija(števec_Gradiva));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(števec_Gradiva.수); System.out.println(하나.isAlive());
        nit_VALUE 셋 = new nit_VALUE(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 zavrniti_VALUE"); }
        System.out.println("nit_VALUE 완료");
    }
}
