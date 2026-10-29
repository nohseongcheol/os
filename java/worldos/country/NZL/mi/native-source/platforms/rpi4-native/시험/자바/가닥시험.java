// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class pūtatau_uara {
    int 수;
    synchronized void 더하기() { int 앞 = 수; Thread.yield(); 수 = 앞 + 1; }
}
class tūmahi_hohenga implements Runnable {
    pūtatau_uara pūtatau_Pūranga_kōrero; tūmahi_hohenga(pūtatau_uara pūtatau_Pūranga_kōrero) { this.pūtatau_Pūranga_kōrero = pūtatau_Pūranga_kōrero; }
    public void run() { for (int i = 0; i < 20; i++) pūtatau_Pūranga_kōrero.더하기(); }
}
class miro_uara extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        pūtatau_uara pūtatau_Pūranga_kōrero = new pūtatau_uara(); Thread 하나 = new Thread(new tūmahi_hohenga(pūtatau_Pūranga_kōrero)); Thread 둘 = new Thread(new tūmahi_hohenga(pūtatau_Pūranga_kōrero));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(pūtatau_Pūranga_kōrero.수); System.out.println(하나.isAlive());
        miro_uara 셋 = new miro_uara(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 거부"); }
        System.out.println("miro_uara 완료");
    }
}
