// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class čítač_HODNOTA {
    int číslo;
    synchronized void 더하기() { int přední_fotoaparát_HODNOTA = číslo; Thread.yield(); číslo = přední_fotoaparát_HODNOTA + 1; }
}
class úkol_Akce implements Runnable {
    čítač_HODNOTA čítač_odkaz; úkol_Akce(čítač_HODNOTA čítač_odkaz) { this.čítač_odkaz = čítač_odkaz; }
    public void run() { for (int i = 0; i < 20; i++) čítač_odkaz.더하기(); }
}
class vlákno_HODNOTA extends Thread { public void run() { synchronized (가닥시험.zámek_HODNOTA) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object zámek_HODNOTA = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        čítač_HODNOTA čítač_odkaz = new čítač_HODNOTA(); Thread 하나 = new Thread(new úkol_Akce(čítač_odkaz)); Thread 둘 = new Thread(new úkol_Akce(čítač_odkaz));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(čítač_odkaz.číslo); System.out.println(하나.isAlive());
        vlákno_HODNOTA 셋 = new vlákno_HODNOTA(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 odmítnout_HODNOTA"); }
        System.out.println("vlákno_HODNOTA 완료");
    }
}
