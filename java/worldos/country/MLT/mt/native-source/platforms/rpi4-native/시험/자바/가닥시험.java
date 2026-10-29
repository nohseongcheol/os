// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class kontatur_VALUE {
    int 수;
    synchronized void 더하기() { int 앞 = 수; Thread.yield(); 수 = 앞 + 1; }
}
class attività_azzjoni implements Runnable {
    kontatur_VALUE kontatur_Referenza; attività_azzjoni(kontatur_VALUE kontatur_Referenza) { this.kontatur_Referenza = kontatur_Referenza; }
    public void run() { for (int i = 0; i < 20; i++) kontatur_Referenza.더하기(); }
}
class fil_VALUE extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        kontatur_VALUE kontatur_Referenza = new kontatur_VALUE(); Thread 하나 = new Thread(new attività_azzjoni(kontatur_Referenza)); Thread 둘 = new Thread(new attività_azzjoni(kontatur_Referenza));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(kontatur_Referenza.수); System.out.println(하나.isAlive());
        fil_VALUE 셋 = new fil_VALUE(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 거부"); }
        System.out.println("fil_VALUE 완료");
    }
}
