// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class sebaledi_Boleng {
    int 수;
    synchronized void 더하기() { int 앞 = 수; Thread.yield(); 수 = 앞 + 1; }
}
class Tiro_tiro implements Runnable {
    sebaledi_Boleng sebaledi_Tshupiso; Tiro_tiro(sebaledi_Boleng sebaledi_Tshupiso) { this.sebaledi_Tshupiso = sebaledi_Tshupiso; }
    public void run() { for (int i = 0; i < 20; i++) sebaledi_Tshupiso.더하기(); }
}
class tlhale_Boleng extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        sebaledi_Boleng sebaledi_Tshupiso = new sebaledi_Boleng(); Thread 하나 = new Thread(new Tiro_tiro(sebaledi_Tshupiso)); Thread 둘 = new Thread(new Tiro_tiro(sebaledi_Tshupiso));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(sebaledi_Tshupiso.수); System.out.println(하나.isAlive());
        tlhale_Boleng 셋 = new tlhale_Boleng(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 거부"); }
        System.out.println("tlhale_Boleng 완료");
    }
}
