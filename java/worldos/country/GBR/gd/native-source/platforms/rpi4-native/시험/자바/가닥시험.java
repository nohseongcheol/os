// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class cunntair_VALUE {
    int 수;
    synchronized void 더하기() { int 앞 = 수; Thread.yield(); 수 = 앞 + 1; }
}
class saothair_gnìomh implements Runnable {
    cunntair_VALUE cunntair_fiosrachadh; saothair_gnìomh(cunntair_VALUE cunntair_fiosrachadh) { this.cunntair_fiosrachadh = cunntair_fiosrachadh; }
    public void run() { for (int i = 0; i < 20; i++) cunntair_fiosrachadh.더하기(); }
}
class snàithlean_VALUE extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        cunntair_VALUE cunntair_fiosrachadh = new cunntair_VALUE(); Thread 하나 = new Thread(new saothair_gnìomh(cunntair_fiosrachadh)); Thread 둘 = new Thread(new saothair_gnìomh(cunntair_fiosrachadh));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(cunntair_fiosrachadh.수); System.out.println(하나.isAlive());
        snàithlean_VALUE 셋 = new snàithlean_VALUE(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 거부"); }
        System.out.println("snàithlean_VALUE 완료");
    }
}
