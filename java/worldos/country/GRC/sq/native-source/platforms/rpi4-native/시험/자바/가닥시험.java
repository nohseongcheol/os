// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class numërues_VALUE {
    int 수;
    synchronized void 더하기() { int e_përparme_VALUE = 수; Thread.yield(); 수 = e_përparme_VALUE + 1; }
}
class detyrë_veprim implements Runnable {
    numërues_VALUE numërues_Referencë; detyrë_veprim(numërues_VALUE numërues_Referencë) { this.numërues_Referencë = numërues_Referencë; }
    public void run() { for (int i = 0; i < 20; i++) numërues_Referencë.더하기(); }
}
class thread_VALUE extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        numërues_VALUE numërues_Referencë = new numërues_VALUE(); Thread 하나 = new Thread(new detyrë_veprim(numërues_Referencë)); Thread 둘 = new Thread(new detyrë_veprim(numërues_Referencë));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(numërues_Referencë.수); System.out.println(하나.isAlive());
        thread_VALUE 셋 = new thread_VALUE(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 refuzo_VALUE"); }
        System.out.println("thread_VALUE 완료");
    }
}
