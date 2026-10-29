// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class skaitītājs_VALUE {
    int numurs;
    synchronized void 더하기() { int priekšējā_VALUE = numurs; Thread.yield(); numurs = priekšējā_VALUE + 1; }
}
class uzdevums_darbība implements Runnable {
    skaitītājs_VALUE skaitītājs_Uzziņas; uzdevums_darbība(skaitītājs_VALUE skaitītājs_Uzziņas) { this.skaitītājs_Uzziņas = skaitītājs_Uzziņas; }
    public void run() { for (int i = 0; i < 20; i++) skaitītājs_Uzziņas.더하기(); }
}
class saruna_VALUE extends Thread { public void run() { synchronized (가닥시험.bloķēt_VALUE) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object bloķēt_VALUE = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        skaitītājs_VALUE skaitītājs_Uzziņas = new skaitītājs_VALUE(); Thread 하나 = new Thread(new uzdevums_darbība(skaitītājs_Uzziņas)); Thread 둘 = new Thread(new uzdevums_darbība(skaitītājs_Uzziņas));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(skaitītājs_Uzziņas.numurs); System.out.println(하나.isAlive());
        saruna_VALUE 셋 = new saruna_VALUE(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 noraidīt_VALUE"); }
        System.out.println("saruna_VALUE 완료");
    }
}
