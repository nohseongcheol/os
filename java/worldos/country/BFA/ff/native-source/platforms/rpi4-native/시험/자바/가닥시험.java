// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class 셈통 {
    int 수;
    synchronized void 더하기() { int 앞 = 수; Thread.yield(); 수 = 앞 + 1; }
}
class golle_gollal implements Runnable {
    셈통 통; golle_gollal(셈통 통) { this.통 = 통; }
    public void run() { for (int i = 0; i < 20; i++) 통.더하기(); }
}
class piilol_njaru extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        셈통 통 = new 셈통(); Thread 하나 = new Thread(new golle_gollal(통)); Thread 둘 = new Thread(new golle_gollal(통));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(통.수); System.out.println(하나.isAlive());
        piilol_njaru 셋 = new piilol_njaru(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 거부"); }
        System.out.println("piilol_njaru 완료");
    }
}
