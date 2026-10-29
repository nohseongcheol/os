// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class kihesabu_thamani {
    int 수;
    synchronized void 더하기() { int mbele_thamani = 수; Thread.yield(); 수 = mbele_thamani + 1; }
}
class kazi_Kitendo implements Runnable {
    kihesabu_thamani kihesabu_Marejeleo; kazi_Kitendo(kihesabu_thamani kihesabu_Marejeleo) { this.kihesabu_Marejeleo = kihesabu_Marejeleo; }
    public void run() { for (int i = 0; i < 20; i++) kihesabu_Marejeleo.더하기(); }
}
class mtungo_thamani extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        kihesabu_thamani kihesabu_Marejeleo = new kihesabu_thamani(); Thread 하나 = new Thread(new kazi_Kitendo(kihesabu_Marejeleo)); Thread 둘 = new Thread(new kazi_Kitendo(kihesabu_Marejeleo));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(kihesabu_Marejeleo.수); System.out.println(하나.isAlive());
        mtungo_thamani 셋 = new mtungo_thamani(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 kataa_thamani"); }
        System.out.println("mtungo_thamani 완료");
    }
}
