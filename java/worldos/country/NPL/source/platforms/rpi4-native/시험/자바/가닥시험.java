// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class बाह्य_आकृति_मान {
    int 수;
    synchronized void 더하기() { int 앞 = 수; Thread.yield(); 수 = 앞 + 1; }
}
class कार्य_कार्य implements Runnable {
    बाह्य_आकृति_मान बाह्य_आकृति_निर्देश; कार्य_कार्य(बाह्य_आकृति_मान बाह्य_आकृति_निर्देश) { this.बाह्य_आकृति_निर्देश = बाह्य_आकृति_निर्देश; }
    public void run() { for (int i = 0; i < 20; i++) बाह्य_आकृति_निर्देश.더하기(); }
}
class धागो_मान extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        बाह्य_आकृति_मान बाह्य_आकृति_निर्देश = new बाह्य_आकृति_मान(); Thread 하나 = new Thread(new कार्य_कार्य(बाह्य_आकृति_निर्देश)); Thread 둘 = new Thread(new कार्य_कार्य(बाह्य_आकृति_निर्देश));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(बाह्य_आकृति_निर्देश.수); System.out.println(하나.isAlive());
        धागो_मान 셋 = new धागो_मान(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 거부"); }
        System.out.println("धागो_मान 완료");
    }
}
