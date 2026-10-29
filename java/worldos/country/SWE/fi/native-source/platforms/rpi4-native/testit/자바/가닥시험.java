// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class laskuri_ARVO {
    int numero;
    synchronized void 더하기() { int etukamera_ARVO = numero; Thread.yield(); numero = etukamera_ARVO + 1; }
}
class tehtävä_toimi implements Runnable {
    laskuri_ARVO laskuri_viite; tehtävä_toimi(laskuri_ARVO laskuri_viite) { this.laskuri_viite = laskuri_viite; }
    public void run() { for (int i = 0; i < 20; i++) laskuri_viite.더하기(); }
}
class säie_ARVO extends Thread { public void run() { synchronized (가닥시험.lukita_ARVO) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object lukita_ARVO = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        laskuri_ARVO laskuri_viite = new laskuri_ARVO(); Thread 하나 = new Thread(new tehtävä_toimi(laskuri_viite)); Thread 둘 = new Thread(new tehtävä_toimi(laskuri_viite));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(laskuri_viite.numero); System.out.println(하나.isAlive());
        säie_ARVO 셋 = new säie_ARVO(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 hylkää_ARVO_e3ecc00b"); }
        System.out.println("säie_ARVO 완료");
    }
}
