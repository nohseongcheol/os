// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class شمار_کنندہ_قدر {
    int 수;
    synchronized void 더하기() { int 앞 = 수; Thread.yield(); 수 = 앞 + 1; }
}
class ٹاسک_عمل implements Runnable {
    شمار_کنندہ_قدر شمار_کنندہ_حوالہ_جات; ٹاسک_عمل(شمار_کنندہ_قدر شمار_کنندہ_حوالہ_جات) { this.شمار_کنندہ_حوالہ_جات = شمار_کنندہ_حوالہ_جات; }
    public void run() { for (int i = 0; i < 20; i++) شمار_کنندہ_حوالہ_جات.더하기(); }
}
class تھریڈ_قدر extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        شمار_کنندہ_قدر شمار_کنندہ_حوالہ_جات = new شمار_کنندہ_قدر(); Thread 하나 = new Thread(new ٹاسک_عمل(شمار_کنندہ_حوالہ_جات)); Thread 둘 = new Thread(new ٹاسک_عمل(شمار_کنندہ_حوالہ_جات));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(شمار_کنندہ_حوالہ_جات.수); System.out.println(하나.isAlive());
        تھریڈ_قدر 셋 = new تھریڈ_قدر(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 رد_کریں_قدر"); }
        System.out.println("تھریڈ_قدر 완료");
    }
}
