// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class áiritheoir_VALUE {
    int 수;
    synchronized void 더하기() { int 앞 = 수; Thread.yield(); 수 = 앞 + 1; }
}
class tasc_gníomh implements Runnable {
    áiritheoir_VALUE áiritheoir_Leabhair_thagartha; tasc_gníomh(áiritheoir_VALUE áiritheoir_Leabhair_thagartha) { this.áiritheoir_Leabhair_thagartha = áiritheoir_Leabhair_thagartha; }
    public void run() { for (int i = 0; i < 20; i++) áiritheoir_Leabhair_thagartha.더하기(); }
}
class snáithe_VALUE extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        áiritheoir_VALUE áiritheoir_Leabhair_thagartha = new áiritheoir_VALUE(); Thread 하나 = new Thread(new tasc_gníomh(áiritheoir_Leabhair_thagartha)); Thread 둘 = new Thread(new tasc_gníomh(áiritheoir_Leabhair_thagartha));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(áiritheoir_Leabhair_thagartha.수); System.out.println(하나.isAlive());
        snáithe_VALUE 셋 = new snáithe_VALUE(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 diúltaigh_VALUE"); }
        System.out.println("snáithe_VALUE 완료");
    }
}
