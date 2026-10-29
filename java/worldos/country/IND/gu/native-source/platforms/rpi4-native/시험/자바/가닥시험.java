// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class ગણક_મૂલ્ય {
    int 수;
    synchronized void 더하기() { int 앞 = 수; Thread.yield(); 수 = 앞 + 1; }
}
class કાર્ય_સંદેશ implements Runnable {
    ગણક_મૂલ્ય ગણક_સંદર્ભ; કાર્ય_સંદેશ(ગણક_મૂલ્ય ગણક_સંદર્ભ) { this.ગણક_સંદર્ભ = ગણક_સંદર્ભ; }
    public void run() { for (int i = 0; i < 20; i++) ગણક_સંદર્ભ.더하기(); }
}
class થ્રેડ_મૂલ્ય extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        ગણક_મૂલ્ય ગણક_સંદર્ભ = new ગણક_મૂલ્ય(); Thread 하나 = new Thread(new કાર્ય_સંદેશ(ગણક_સંદર્ભ)); Thread 둘 = new Thread(new કાર્ય_સંદેશ(ગણક_સંદર્ભ));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(ગણક_સંદર્ભ.수); System.out.println(하나.isAlive());
        થ્રેડ_મૂલ્ય 셋 = new થ્રેડ_મૂલ્ય(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 નકારો_મૂલ્ય"); }
        System.out.println("થ્રેડ_મૂલ્ય 완료");
    }
}
