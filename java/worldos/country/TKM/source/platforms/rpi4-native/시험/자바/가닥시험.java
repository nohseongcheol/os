// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class sanaýjy_baha {
    int 수;
    synchronized void 더하기() { int 앞 = 수; Thread.yield(); 수 = 앞 + 1; }
}
class tabşyryk_iş implements Runnable {
    sanaýjy_baha sanaýjy_Salgylanma; tabşyryk_iş(sanaýjy_baha sanaýjy_Salgylanma) { this.sanaýjy_Salgylanma = sanaýjy_Salgylanma; }
    public void run() { for (int i = 0; i < 20; i++) sanaýjy_Salgylanma.더하기(); }
}
class akym_baha extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        sanaýjy_baha sanaýjy_Salgylanma = new sanaýjy_baha(); Thread 하나 = new Thread(new tabşyryk_iş(sanaýjy_Salgylanma)); Thread 둘 = new Thread(new tabşyryk_iş(sanaýjy_Salgylanma));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(sanaýjy_Salgylanma.수); System.out.println(하나.isAlive());
        akym_baha 셋 = new akym_baha(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 거부"); }
        System.out.println("akym_baha 완료");
    }
}
