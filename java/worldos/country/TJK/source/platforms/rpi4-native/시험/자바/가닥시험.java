// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class ҳисобкунак_қимат {
    int 수;
    synchronized void 더하기() { int 앞 = 수; Thread.yield(); 수 = 앞 + 1; }
}
class вазифа_амал implements Runnable {
    ҳисобкунак_қимат ҳисобкунак_Маълумотнома; вазифа_амал(ҳисобкунак_қимат ҳисобкунак_Маълумотнома) { this.ҳисобкунак_Маълумотнома = ҳисобкунак_Маълумотнома; }
    public void run() { for (int i = 0; i < 20; i++) ҳисобкунак_Маълумотнома.더하기(); }
}
class ришта_қимат extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        ҳисобкунак_қимат ҳисобкунак_Маълумотнома = new ҳисобкунак_қимат(); Thread 하나 = new Thread(new вазифа_амал(ҳисобкунак_Маълумотнома)); Thread 둘 = new Thread(new вазифа_амал(ҳисобкунак_Маълумотнома));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(ҳисобкунак_Маълумотнома.수); System.out.println(하나.isAlive());
        ришта_қимат 셋 = new ришта_қимат(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 거부"); }
        System.out.println("ришта_қимат 완료");
    }
}
