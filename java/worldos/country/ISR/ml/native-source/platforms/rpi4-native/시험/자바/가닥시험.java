// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class కౌంటర్_മൂല്യം {
    int 수;
    synchronized void 더하기() { int മുൻവശം_മൂല്യം = 수; Thread.yield(); 수 = മുൻവശം_മൂല്യം + 1; }
}
class ചുമതല_ക്രിയ implements Runnable {
    కౌంటర్_മൂല്യം కౌంటర్_റഫറൻസ്; ചുമതല_ക്രിയ(కౌంటర్_മൂല്യം కౌంటర్_റഫറൻസ്) { this.కౌంటర్_റഫറൻസ് = కౌంటర్_റഫറൻസ്; }
    public void run() { for (int i = 0; i < 20; i++) కౌంటర్_റഫറൻസ്.더하기(); }
}
class ത്രെഡ്_മൂല്യം extends Thread { public void run() { synchronized (가닥시험.ലോക്ക്_മൂല്യം) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object ലോക്ക്_മൂല്യം = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        కౌంటర్_മൂല്യം కౌంటర్_റഫറൻസ് = new కౌంటర్_മൂല്യം(); Thread 하나 = new Thread(new ചുമതല_ക്രിയ(కౌంటర్_റഫറൻസ്)); Thread 둘 = new Thread(new ചുമതല_ക്രിയ(కౌంటర్_റഫറൻസ്));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(కౌంటర్_റഫറൻസ്.수); System.out.println(하나.isAlive());
        ത്രെഡ്_മൂല്യം 셋 = new ത്രെഡ്_മൂല്യം(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 നിരസിക്കുക_മൂല്യം"); }
        System.out.println("ത്രെഡ്_മൂല്യം 완료");
    }
}
