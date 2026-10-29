// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class شمارنده_مقدار {
    int 수;
    synchronized void 더하기() { int جلو_مقدار = 수; Thread.yield(); 수 = جلو_مقدار + 1; }
}
class کار_عمل implements Runnable {
    شمارنده_مقدار شمارنده_مرجع; کار_عمل(شمارنده_مقدار شمارنده_مرجع) { this.شمارنده_مرجع = شمارنده_مرجع; }
    public void run() { for (int i = 0; i < 20; i++) شمارنده_مرجع.더하기(); }
}
class رشته_مقدار extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        شمارنده_مقدار شمارنده_مرجع = new شمارنده_مقدار(); Thread 하나 = new Thread(new کار_عمل(شمارنده_مرجع)); Thread 둘 = new Thread(new کار_عمل(شمارنده_مرجع));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(شمارنده_مرجع.수); System.out.println(하나.isAlive());
        رشته_مقدار 셋 = new رشته_مقدار(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 رد_کردن_مقدار"); }
        System.out.println("رشته_مقدار 완료");
    }
}
