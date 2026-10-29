// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class isibali_inani {
    int 수;
    synchronized void 더하기() { int 앞 = 수; Thread.yield(); 수 = 앞 + 1; }
}
class umsebenzi_isenzo implements Runnable {
    isibali_inani isibali_Ireferensi; umsebenzi_isenzo(isibali_inani isibali_Ireferensi) { this.isibali_Ireferensi = isibali_Ireferensi; }
    public void run() { for (int i = 0; i < 20; i++) isibali_Ireferensi.더하기(); }
}
class uhlu_lwemilayezo_inani extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        isibali_inani isibali_Ireferensi = new isibali_inani(); Thread 하나 = new Thread(new umsebenzi_isenzo(isibali_Ireferensi)); Thread 둘 = new Thread(new umsebenzi_isenzo(isibali_Ireferensi));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(isibali_Ireferensi.수); System.out.println(하나.isAlive());
        uhlu_lwemilayezo_inani 셋 = new uhlu_lwemilayezo_inani(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 거부"); }
        System.out.println("uhlu_lwemilayezo_inani 완료");
    }
}
