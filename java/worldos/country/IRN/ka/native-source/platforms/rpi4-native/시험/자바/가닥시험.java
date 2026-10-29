// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class მრიცხველი_მნიშვნელობა {
    int 수;
    synchronized void 더하기() { int 앞 = 수; Thread.yield(); 수 = 앞 + 1; }
}
class დავალება_მოქმედება implements Runnable {
    მრიცხველი_მნიშვნელობა მრიცხველი_ცნობარები; დავალება_მოქმედება(მრიცხველი_მნიშვნელობა მრიცხველი_ცნობარები) { this.მრიცხველი_ცნობარები = მრიცხველი_ცნობარები; }
    public void run() { for (int i = 0; i < 20; i++) მრიცხველი_ცნობარები.더하기(); }
}
class თემა_მნიშვნელობა extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        მრიცხველი_მნიშვნელობა მრიცხველი_ცნობარები = new მრიცხველი_მნიშვნელობა(); Thread 하나 = new Thread(new დავალება_მოქმედება(მრიცხველი_ცნობარები)); Thread 둘 = new Thread(new დავალება_მოქმედება(მრიცხველი_ცნობარები));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(მრიცხველი_ცნობარები.수); System.out.println(하나.isAlive());
        თემა_მნიშვნელობა 셋 = new თემა_მნიშვნელობა(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 거부"); }
        System.out.println("თემა_მნიშვნელობა 완료");
    }
}
