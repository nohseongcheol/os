// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class лічыльнік_значэнне {
    int 수;
    synchronized void 더하기() { int пярэдняя_камера_значэнне = 수; Thread.yield(); 수 = пярэдняя_камера_значэнне + 1; }
}
class задача_дзеянне implements Runnable {
    лічыльнік_значэнне лічыльнік_Даведачныя_матэрыялы; задача_дзеянне(лічыльнік_значэнне лічыльнік_Даведачныя_матэрыялы) { this.лічыльнік_Даведачныя_матэрыялы = лічыльнік_Даведачныя_матэрыялы; }
    public void run() { for (int i = 0; i < 20; i++) лічыльнік_Даведачныя_матэрыялы.더하기(); }
}
class паток_значэнне_5b72a632 extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        лічыльнік_значэнне лічыльнік_Даведачныя_матэрыялы = new лічыльнік_значэнне(); Thread 하나 = new Thread(new задача_дзеянне(лічыльнік_Даведачныя_матэрыялы)); Thread 둘 = new Thread(new задача_дзеянне(лічыльнік_Даведачныя_матэрыялы));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(лічыльнік_Даведачныя_матэрыялы.수); System.out.println(하나.isAlive());
        паток_значэнне_5b72a632 셋 = new паток_значэнне_5b72a632(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 адхіліць_значэнне"); }
        System.out.println("паток_значэнне_5b72a632 완료");
    }
}
