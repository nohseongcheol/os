// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class contor_VALUE {
    int 수;
    synchronized void 더하기() { int frontală_VALUE = 수; Thread.yield(); 수 = frontală_VALUE + 1; }
}
class sarcină_Acțiune implements Runnable {
    contor_VALUE contor_referință; sarcină_Acțiune(contor_VALUE contor_referință) { this.contor_referință = contor_referință; }
    public void run() { for (int i = 0; i < 20; i++) contor_referință.더하기(); }
}
class fir_VALUE extends Thread { public void run() { synchronized (가닥시험.blocare_VALUE) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object blocare_VALUE = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        contor_VALUE contor_referință = new contor_VALUE(); Thread 하나 = new Thread(new sarcină_Acțiune(contor_referință)); Thread 둘 = new Thread(new sarcină_Acțiune(contor_referință));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(contor_referință.수); System.out.println(하나.isAlive());
        fir_VALUE 셋 = new fir_VALUE(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 respinge_VALUE"); }
        System.out.println("fir_VALUE 완료");
    }
}
