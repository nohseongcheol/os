// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class брояч_стойност {
    int 수;
    synchronized void 더하기() { int предна_стойност = 수; Thread.yield(); 수 = предна_стойност + 1; }
}
class задача_проект implements Runnable {
    брояч_стойност брояч_препратка; задача_проект(брояч_стойност брояч_препратка) { this.брояч_препратка = брояч_препратка; }
    public void run() { for (int i = 0; i < 20; i++) брояч_препратка.더하기(); }
}
class нишка_стойност extends Thread { public void run() { synchronized (가닥시험.заключване_стойност) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object заключване_стойност = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        брояч_стойност брояч_препратка = new брояч_стойност(); Thread 하나 = new Thread(new задача_проект(брояч_препратка)); Thread 둘 = new Thread(new задача_проект(брояч_препратка));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(брояч_препратка.수); System.out.println(하나.isAlive());
        нишка_стойност 셋 = new нишка_стойност(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 отхвърлям_стойност_e3ecc00b"); }
        System.out.println("нишка_стойност 완료");
    }
}
