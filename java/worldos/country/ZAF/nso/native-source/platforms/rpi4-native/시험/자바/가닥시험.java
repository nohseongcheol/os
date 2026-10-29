// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class sebadi_boleng {
    int 수;
    synchronized void 더하기() { int 앞 = 수; Thread.yield(); 수 = 앞 + 1; }
}
class mošomo_tiro implements Runnable {
    sebadi_boleng sebadi_Dipadišo; mošomo_tiro(sebadi_boleng sebadi_Dipadišo) { this.sebadi_Dipadišo = sebadi_Dipadišo; }
    public void run() { for (int i = 0; i < 20; i++) sebadi_Dipadišo.더하기(); }
}
class threte_boleng extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        sebadi_boleng sebadi_Dipadišo = new sebadi_boleng(); Thread 하나 = new Thread(new mošomo_tiro(sebadi_Dipadišo)); Thread 둘 = new Thread(new mošomo_tiro(sebadi_Dipadišo));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(sebadi_Dipadišo.수); System.out.println(하나.isAlive());
        threte_boleng 셋 = new threte_boleng(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 거부"); }
        System.out.println("threte_boleng 완료");
    }
}
