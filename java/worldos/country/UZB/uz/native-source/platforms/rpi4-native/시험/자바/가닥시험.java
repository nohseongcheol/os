// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class hisoblagich_VALUE {
    int 수;
    synchronized void 더하기() { int old_kamera_VALUE = 수; Thread.yield(); 수 = old_kamera_VALUE + 1; }
}
class vazifa_harakat implements Runnable {
    hisoblagich_VALUE hisoblagich_Ma_lumotnomalar; vazifa_harakat(hisoblagich_VALUE hisoblagich_Ma_lumotnomalar) { this.hisoblagich_Ma_lumotnomalar = hisoblagich_Ma_lumotnomalar; }
    public void run() { for (int i = 0; i < 20; i++) hisoblagich_Ma_lumotnomalar.더하기(); }
}
class oqim_VALUE_5b72a632 extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        hisoblagich_VALUE hisoblagich_Ma_lumotnomalar = new hisoblagich_VALUE(); Thread 하나 = new Thread(new vazifa_harakat(hisoblagich_Ma_lumotnomalar)); Thread 둘 = new Thread(new vazifa_harakat(hisoblagich_Ma_lumotnomalar));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(hisoblagich_Ma_lumotnomalar.수); System.out.println(하나.isAlive());
        oqim_VALUE_5b72a632 셋 = new oqim_VALUE_5b72a632(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 거부"); }
        System.out.println("oqim_VALUE_5b72a632 완료");
    }
}
