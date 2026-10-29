// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class rhifydd_VALUE {
    int 수;
    synchronized void 더하기() { int 앞 = 수; Thread.yield(); 수 = 앞 + 1; }
}
class tasg_gweithred implements Runnable {
    rhifydd_VALUE rhifydd_cyfeiriad; tasg_gweithred(rhifydd_VALUE rhifydd_cyfeiriad) { this.rhifydd_cyfeiriad = rhifydd_cyfeiriad; }
    public void run() { for (int i = 0; i < 20; i++) rhifydd_cyfeiriad.더하기(); }
}
class edefyn_VALUE extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        rhifydd_VALUE rhifydd_cyfeiriad = new rhifydd_VALUE(); Thread 하나 = new Thread(new tasg_gweithred(rhifydd_cyfeiriad)); Thread 둘 = new Thread(new tasg_gweithred(rhifydd_cyfeiriad));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(rhifydd_cyfeiriad.수); System.out.println(하나.isAlive());
        edefyn_VALUE 셋 = new edefyn_VALUE(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 gwrthod_VALUE"); }
        System.out.println("edefyn_VALUE 완료");
    }
}
