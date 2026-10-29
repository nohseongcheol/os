// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class counter_VALUE {
    int 수;
    synchronized void 더하기() { int nasa_harap_VALUE = 수; Thread.yield(); 수 = nasa_harap_VALUE + 1; }
}
class gawain_aksyon implements Runnable {
    counter_VALUE counter_Sanggunian; gawain_aksyon(counter_VALUE counter_Sanggunian) { this.counter_Sanggunian = counter_Sanggunian; }
    public void run() { for (int i = 0; i < 20; i++) counter_Sanggunian.더하기(); }
}
class thread_VALUE extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        counter_VALUE counter_Sanggunian = new counter_VALUE(); Thread 하나 = new Thread(new gawain_aksyon(counter_Sanggunian)); Thread 둘 = new Thread(new gawain_aksyon(counter_Sanggunian));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(counter_Sanggunian.수); System.out.println(하나.isAlive());
        thread_VALUE 셋 = new thread_VALUE(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 tanggihan_VALUE"); }
        System.out.println("thread_VALUE 완료");
    }
}
