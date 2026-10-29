// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class ژمێرەر_نرخ {
    int 수;
    synchronized void 더하기() { int 앞 = 수; Thread.yield(); 수 = 앞 + 1; }
}
class ئەرک_ئاکشن implements Runnable {
    ژمێرەر_نرخ ژمێرەر_سەرچاوە; ئەرک_ئاکشن(ژمێرەر_نرخ ژمێرەر_سەرچاوە) { this.ژمێرەر_سەرچاوە = ژمێرەر_سەرچاوە; }
    public void run() { for (int i = 0; i < 20; i++) ژمێرەر_سەرچاوە.더하기(); }
}
class ڕستە_نرخ extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        ژمێرەر_نرخ ژمێرەر_سەرچاوە = new ژمێرەر_نرخ(); Thread 하나 = new Thread(new ئەرک_ئاکشن(ژمێرەر_سەرچاوە)); Thread 둘 = new Thread(new ئەرک_ئاکشن(ژمێرەر_سەرچاوە));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(ژمێرەر_سەرچاوە.수); System.out.println(하나.isAlive());
        ڕستە_نرخ 셋 = new ڕستە_نرخ(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 거부"); }
        System.out.println("ڕستە_نرخ 완료");
    }
}
