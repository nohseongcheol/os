// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class besoekteller_VALUE {
    int 수;
    synchronized void 더하기() { int voor_VALUE = 수; Thread.yield(); 수 = voor_VALUE + 1; }
}
class taak_aksie implements Runnable {
    besoekteller_VALUE besoekteller_Naslaan; taak_aksie(besoekteller_VALUE besoekteller_Naslaan) { this.besoekteller_Naslaan = besoekteller_Naslaan; }
    public void run() { for (int i = 0; i < 20; i++) besoekteller_Naslaan.더하기(); }
}
class draad_VALUE extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        besoekteller_VALUE besoekteller_Naslaan = new besoekteller_VALUE(); Thread 하나 = new Thread(new taak_aksie(besoekteller_Naslaan)); Thread 둘 = new Thread(new taak_aksie(besoekteller_Naslaan));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(besoekteller_Naslaan.수); System.out.println(하나.isAlive());
        draad_VALUE 셋 = new draad_VALUE(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 거부"); }
        System.out.println("draad_VALUE 완료");
    }
}
