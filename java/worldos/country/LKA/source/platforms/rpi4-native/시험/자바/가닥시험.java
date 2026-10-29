// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class ගණකය_අගය {
    int 수;
    synchronized void 더하기() { int 앞 = 수; Thread.yield(); 수 = 앞 + 1; }
}
class කාර්යය_ක්_රියාව implements Runnable {
    ගණකය_අගය ගණකය_පරිශීලනය; කාර්යය_ක්_රියාව(ගණකය_අගය ගණකය_පරිශීලනය) { this.ගණකය_පරිශීලනය = ගණකය_පරිශීලනය; }
    public void run() { for (int i = 0; i < 20; i++) ගණකය_පරිශීලනය.더하기(); }
}
class පොට_අගය extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        ගණකය_අගය ගණකය_පරිශීලනය = new ගණකය_අගය(); Thread 하나 = new Thread(new කාර්යය_ක්_රියාව(ගණකය_පරිශීලනය)); Thread 둘 = new Thread(new කාර්යය_ක්_රියාව(ගණකය_පරිශීලනය));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(ගණකය_පරිශීලනය.수); System.out.println(하나.isAlive());
        පොට_අගය 셋 = new පොට_අගය(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 거부"); }
        System.out.println("පොට_අගය 완료");
    }
}
