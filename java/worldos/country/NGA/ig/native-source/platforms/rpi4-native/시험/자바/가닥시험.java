// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class ǹgụ_valuu {
    int 수;
    synchronized void 더하기() { int 앞 = 수; Thread.yield(); 수 = 앞 + 1; }
}
class ọrụ_mmèm implements Runnable {
    ǹgụ_valuu ǹgụ_Nrụtụ_aka; ọrụ_mmèm(ǹgụ_valuu ǹgụ_Nrụtụ_aka) { this.ǹgụ_Nrụtụ_aka = ǹgụ_Nrụtụ_aka; }
    public void run() { for (int i = 0; i < 20; i++) ǹgụ_Nrụtụ_aka.더하기(); }
}
class treèd_valuu extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        ǹgụ_valuu ǹgụ_Nrụtụ_aka = new ǹgụ_valuu(); Thread 하나 = new Thread(new ọrụ_mmèm(ǹgụ_Nrụtụ_aka)); Thread 둘 = new Thread(new ọrụ_mmèm(ǹgụ_Nrụtụ_aka));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(ǹgụ_Nrụtụ_aka.수); System.out.println(하나.isAlive());
        treèd_valuu 셋 = new treèd_valuu(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 거부"); }
        System.out.println("treèd_valuu 완료");
    }
}
