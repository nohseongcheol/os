// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class গণক_মান {
    int 수;
    synchronized void 더하기() { int সম্মুখ_মান = 수; Thread.yield(); 수 = সম্মুখ_মান + 1; }
}
class কার্য_কর্ম implements Runnable {
    গণক_মান গণক_প্রসঙ্গ; কার্য_কর্ম(গণক_মান গণক_প্রসঙ্গ) { this.গণক_প্রসঙ্গ = গণক_প্রসঙ্গ; }
    public void run() { for (int i = 0; i < 20; i++) গণক_প্রসঙ্গ.더하기(); }
}
class থ্রেড_মান extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        গণক_মান গণক_প্রসঙ্গ = new গণক_মান(); Thread 하나 = new Thread(new কার্য_কর্ম(গণক_প্রসঙ্গ)); Thread 둘 = new Thread(new কার্য_কর্ম(গণক_প্রসঙ্গ));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(গণক_প্রসঙ্গ.수); System.out.println(하나.isAlive());
        থ্রেড_মান 셋 = new থ্রেড_মান(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 প্রত্যাখ্যান_মান"); }
        System.out.println("থ্রেড_মান 완료");
    }
}
