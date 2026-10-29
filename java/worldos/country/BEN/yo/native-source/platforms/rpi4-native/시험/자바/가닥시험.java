// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class òǹkà_iye {
    int 수;
    synchronized void 더하기() { int 앞 = 수; Thread.yield(); 수 = 앞 + 1; }
}
class iṣẹ́_ìṣe implements Runnable {
    òǹkà_iye òǹkà_Ìtọ́ka; iṣẹ́_ìṣe(òǹkà_iye òǹkà_Ìtọ́ka) { this.òǹkà_Ìtọ́ka = òǹkà_Ìtọ́ka; }
    public void run() { for (int i = 0; i < 20; i++) òǹkà_Ìtọ́ka.더하기(); }
}
class èròjà_atẹ̀lélànà_iye extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        òǹkà_iye òǹkà_Ìtọ́ka = new òǹkà_iye(); Thread 하나 = new Thread(new iṣẹ́_ìṣe(òǹkà_Ìtọ́ka)); Thread 둘 = new Thread(new iṣẹ́_ìṣe(òǹkà_Ìtọ́ka));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(òǹkà_Ìtọ́ka.수); System.out.println(하나.isAlive());
        èròjà_atẹ̀lélànà_iye 셋 = new èròjà_atẹ̀lélànà_iye(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 거부"); }
        System.out.println("èròjà_atẹ̀lélànà_iye 완료");
    }
}
