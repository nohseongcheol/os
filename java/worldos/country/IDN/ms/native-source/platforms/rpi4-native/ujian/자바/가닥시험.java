// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class 셈통 {
    int 수;
    synchronized void 더하기() { int hadapan_VALUE = 수; Thread.yield(); 수 = hadapan_VALUE + 1; }
}
class tugas_cadangan implements Runnable {
    셈통 통; tugas_cadangan(셈통 통) { this.통 = 통; }
    public void run() { for (int i = 0; i < 20; i++) 통.더하기(); }
}
class urutan_VALUE extends Thread { public void run() { synchronized (가닥시험.kunci_VALUE) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object kunci_VALUE = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        셈통 통 = new 셈통(); Thread 하나 = new Thread(new tugas_cadangan(통)); Thread 둘 = new Thread(new tugas_cadangan(통));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(통.수); System.out.println(하나.isAlive());
        urutan_VALUE 셋 = new urutan_VALUE(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 tolak_VALUE"); }
        System.out.println("urutan_VALUE 완료");
    }
}
