// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class loendur_VALUE {
    int number;
    synchronized void 더하기() { int esikaamera_VALUE = number; Thread.yield(); number = esikaamera_VALUE + 1; }
}
class tööüksus_Toiming implements Runnable {
    loendur_VALUE loendur_viide; tööüksus_Toiming(loendur_VALUE loendur_viide) { this.loendur_viide = loendur_viide; }
    public void run() { for (int i = 0; i < 20; i++) loendur_viide.더하기(); }
}
class lõim_VALUE extends Thread { public void run() { synchronized (가닥시험.lukk_VALUE) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object lukk_VALUE = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        loendur_VALUE loendur_viide = new loendur_VALUE(); Thread 하나 = new Thread(new tööüksus_Toiming(loendur_viide)); Thread 둘 = new Thread(new tööüksus_Toiming(loendur_viide));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(loendur_viide.number); System.out.println(하나.isAlive());
        lõim_VALUE 셋 = new lõim_VALUE(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 keelduma_VALUE"); }
        System.out.println("lõim_VALUE 완료");
    }
}
