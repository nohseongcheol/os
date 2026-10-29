// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class számláló_ÉRTÉK {
    int szám;
    synchronized void 더하기() { int elülső_kamera_ÉRTÉK = szám; Thread.yield(); szám = elülső_kamera_ÉRTÉK + 1; }
}
class teendő_Action implements Runnable {
    számláló_ÉRTÉK számláló_hivatkozik; teendő_Action(számláló_ÉRTÉK számláló_hivatkozik) { this.számláló_hivatkozik = számláló_hivatkozik; }
    public void run() { for (int i = 0; i < 20; i++) számláló_hivatkozik.더하기(); }
}
class szál_ÉRTÉK extends Thread { public void run() { synchronized (가닥시험.lezár_ÉRTÉK) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object lezár_ÉRTÉK = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        számláló_ÉRTÉK számláló_hivatkozik = new számláló_ÉRTÉK(); Thread 하나 = new Thread(new teendő_Action(számláló_hivatkozik)); Thread 둘 = new Thread(new teendő_Action(számláló_hivatkozik));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(számláló_hivatkozik.szám); System.out.println(하나.isAlive());
        szál_ÉRTÉK 셋 = new szál_ÉRTÉK(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 elutasít_ÉRTÉK"); }
        System.out.println("szál_ÉRTÉK 완료");
    }
}
