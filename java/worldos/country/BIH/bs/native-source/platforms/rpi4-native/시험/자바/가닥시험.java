// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class brojač_VALUE {
    int 수;
    synchronized void 더하기() { int 앞 = 수; Thread.yield(); 수 = 앞 + 1; }
}
class zadatak_radnja implements Runnable {
    brojač_VALUE brojač_Reference; zadatak_radnja(brojač_VALUE brojač_Reference) { this.brojač_Reference = brojač_Reference; }
    public void run() { for (int i = 0; i < 20; i++) brojač_Reference.더하기(); }
}
class nit_VALUE extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        brojač_VALUE brojač_Reference = new brojač_VALUE(); Thread 하나 = new Thread(new zadatak_radnja(brojač_Reference)); Thread 둘 = new Thread(new zadatak_radnja(brojač_Reference));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(brojač_Reference.수); System.out.println(하나.isAlive());
        nit_VALUE 셋 = new nit_VALUE(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 odbiti_VALUE"); }
        System.out.println("nit_VALUE 완료");
    }
}
