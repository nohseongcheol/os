// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class teljari_VALUE {
    int númer;
    synchronized void 더하기() { int myndavél_að_framan_VALUE = númer; Thread.yield(); númer = myndavél_að_framan_VALUE + 1; }
}
class verk_aðgerð implements Runnable {
    teljari_VALUE teljari_tilvísun; verk_aðgerð(teljari_VALUE teljari_tilvísun) { this.teljari_tilvísun = teljari_tilvísun; }
    public void run() { for (int i = 0; i < 20; i++) teljari_tilvísun.더하기(); }
}
class þráður_VALUE extends Thread { public void run() { synchronized (가닥시험.Loka_VALUE) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object Loka_VALUE = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        teljari_VALUE teljari_tilvísun = new teljari_VALUE(); Thread 하나 = new Thread(new verk_aðgerð(teljari_tilvísun)); Thread 둘 = new Thread(new verk_aðgerð(teljari_tilvísun));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(teljari_tilvísun.númer); System.out.println(하나.isAlive());
        þráður_VALUE 셋 = new þráður_VALUE(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 hafna_VALUE"); }
        System.out.println("þráður_VALUE 완료");
    }
}
