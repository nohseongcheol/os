// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class waññukaay_xëyma {
    int 수;
    synchronized void 더하기() { int 앞 = 수; Thread.yield(); 수 = 앞 + 1; }
}
class ligeey_jëf implements Runnable {
    waññukaay_xëyma waññukaay_Royukaay; ligeey_jëf(waññukaay_xëyma waññukaay_Royukaay) { this.waññukaay_Royukaay = waññukaay_Royukaay; }
    public void run() { for (int i = 0; i < 20; i++) waññukaay_Royukaay.더하기(); }
}
class buumug_jokkale_xëyma extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        waññukaay_xëyma waññukaay_Royukaay = new waññukaay_xëyma(); Thread 하나 = new Thread(new ligeey_jëf(waññukaay_Royukaay)); Thread 둘 = new Thread(new ligeey_jëf(waññukaay_Royukaay));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(waññukaay_Royukaay.수); System.out.println(하나.isAlive());
        buumug_jokkale_xëyma 셋 = new buumug_jokkale_xëyma(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 거부"); }
        System.out.println("buumug_jokkale_xëyma 완료");
    }
}
