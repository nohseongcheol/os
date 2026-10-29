// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class కౌంటర్_మూల్యం {
    int 수;
    synchronized void 더하기() { int ముందు_మూల్యం = 수; Thread.yield(); 수 = ముందు_మూల్యం + 1; }
}
class విధి_చర్య implements Runnable {
    కౌంటర్_మూల్యం కౌంటర్_సూచన; విధి_చర్య(కౌంటర్_మూల్యం కౌంటర్_సూచన) { this.కౌంటర్_సూచన = కౌంటర్_సూచన; }
    public void run() { for (int i = 0; i < 20; i++) కౌంటర్_సూచన.더하기(); }
}
class థ్రెడ్_మూల్యం extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        కౌంటర్_మూల్యం కౌంటర్_సూచన = new కౌంటర్_మూల్యం(); Thread 하나 = new Thread(new విధి_చర్య(కౌంటర్_సూచన)); Thread 둘 = new Thread(new విధి_చర్య(కౌంటర్_సూచన));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(కౌంటర్_సూచన.수); System.out.println(하나.isAlive());
        థ్రెడ్_మూల్యం 셋 = new థ్రెడ్_మూల్యం(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 తిరస్కరించు_మూల్యం"); }
        System.out.println("థ్రెడ్_మూల్యం 완료");
    }
}
