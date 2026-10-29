// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class شمار_کرنڑ_آلا_قدر {
    int 수;
    synchronized void 더하기() { int 앞 = 수; Thread.yield(); 수 = 앞 + 1; }
}
class ٹاسک_کم implements Runnable {
    شمار_کرنڑ_آلا_قدر شمار_کرنڑ_آلا_حوالہ; ٹاسک_کم(شمار_کرنڑ_آلا_قدر شمار_کرنڑ_آلا_حوالہ) { this.شمار_کرنڑ_آلا_حوالہ = شمار_کرنڑ_آلا_حوالہ; }
    public void run() { for (int i = 0; i < 20; i++) شمار_کرنڑ_آلا_حوالہ.더하기(); }
}
class لڑی_قدر extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        شمار_کرنڑ_آلا_قدر شمار_کرنڑ_آلا_حوالہ = new شمار_کرنڑ_آلا_قدر(); Thread 하나 = new Thread(new ٹاسک_کم(شمار_کرنڑ_آلا_حوالہ)); Thread 둘 = new Thread(new ٹاسک_کم(شمار_کرنڑ_آلا_حوالہ));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(شمار_کرنڑ_آلا_حوالہ.수); System.out.println(하나.isAlive());
        لڑی_قدر 셋 = new لڑی_قدر(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 거부"); }
        System.out.println("لڑی_قدر 완료");
    }
}
