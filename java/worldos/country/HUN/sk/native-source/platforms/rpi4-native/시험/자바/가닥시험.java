// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class počítadlo_VALUE {
    int 수;
    synchronized void 더하기() { int predný_VALUE = 수; Thread.yield(); 수 = predný_VALUE + 1; }
}
class úloha_Akcia implements Runnable {
    počítadlo_VALUE počítadlo_zdroj; úloha_Akcia(počítadlo_VALUE počítadlo_zdroj) { this.počítadlo_zdroj = počítadlo_zdroj; }
    public void run() { for (int i = 0; i < 20; i++) počítadlo_zdroj.더하기(); }
}
class vlákno_VALUE extends Thread { public void run() { synchronized (가닥시험.zámok_VALUE) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object zámok_VALUE = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        počítadlo_VALUE počítadlo_zdroj = new počítadlo_VALUE(); Thread 하나 = new Thread(new úloha_Akcia(počítadlo_zdroj)); Thread 둘 = new Thread(new úloha_Akcia(počítadlo_zdroj));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(počítadlo_zdroj.수); System.out.println(하나.isAlive());
        vlákno_VALUE 셋 = new vlákno_VALUE(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 odmietnuť_VALUE"); }
        System.out.println("vlákno_VALUE 완료");
    }
}
