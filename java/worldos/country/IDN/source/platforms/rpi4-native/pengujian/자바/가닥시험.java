// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class penghitung_VALUE {
    int 수;
    synchronized void 더하기() { int depan_VALUE = 수; Thread.yield(); 수 = depan_VALUE + 1; }
}
class tugas_Tugas implements Runnable {
    penghitung_VALUE penghitung_Referensi; tugas_Tugas(penghitung_VALUE penghitung_Referensi) { this.penghitung_Referensi = penghitung_Referensi; }
    public void run() { for (int i = 0; i < 20; i++) penghitung_Referensi.더하기(); }
}
class alur_VALUE extends Thread { public void run() { synchronized (가닥시험.kunci_VALUE) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object kunci_VALUE = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        penghitung_VALUE penghitung_Referensi = new penghitung_VALUE(); Thread 하나 = new Thread(new tugas_Tugas(penghitung_Referensi)); Thread 둘 = new Thread(new tugas_Tugas(penghitung_Referensi));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(penghitung_Referensi.수); System.out.println(하나.isAlive());
        alur_VALUE 셋 = new alur_VALUE(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 tolak_VALUE"); }
        System.out.println("alur_VALUE 완료");
    }
}
