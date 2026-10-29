// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class brojač_VALUE {
    int 수;
    synchronized void 더하기() { int čeona_kamera_VALUE = 수; Thread.yield(); 수 = čeona_kamera_VALUE + 1; }
}
class obaveza_radnja implements Runnable {
    brojač_VALUE brojač_referenca; obaveza_radnja(brojač_VALUE brojač_referenca) { this.brojač_referenca = brojač_referenca; }
    public void run() { for (int i = 0; i < 20; i++) brojač_referenca.더하기(); }
}
class nit_VALUE extends Thread { public void run() { synchronized (가닥시험.zaključati_VALUE) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object zaključati_VALUE = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        brojač_VALUE brojač_referenca = new brojač_VALUE(); Thread 하나 = new Thread(new obaveza_radnja(brojač_referenca)); Thread 둘 = new Thread(new obaveza_radnja(brojač_referenca));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(brojač_referenca.수); System.out.println(하나.isAlive());
        nit_VALUE 셋 = new nit_VALUE(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 odbaciti_VALUE_e3ecc00b"); }
        System.out.println("nit_VALUE 완료");
    }
}
