// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class есептегіш_мән {
    int 수;
    synchronized void 더하기() { int алдыңғы_камера_мән = 수; Thread.yield(); 수 = алдыңғы_камера_мән + 1; }
}
class тапсырма_ұсыныс implements Runnable {
    есептегіш_мән есептегіш_Анықтамалық; тапсырма_ұсыныс(есептегіш_мән есептегіш_Анықтамалық) { this.есептегіш_Анықтамалық = есептегіш_Анықтамалық; }
    public void run() { for (int i = 0; i < 20; i++) есептегіш_Анықтамалық.더하기(); }
}
class ағын_мән extends Thread { public void run() { synchronized (가닥시험.блоктау_мән) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object блоктау_мән = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        есептегіш_мән есептегіш_Анықтамалық = new есептегіш_мән(); Thread 하나 = new Thread(new тапсырма_ұсыныс(есептегіш_Анықтамалық)); Thread 둘 = new Thread(new тапсырма_ұсыныс(есептегіш_Анықтамалық));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(есептегіш_Анықтамалық.수); System.out.println(하나.isAlive());
        ағын_мән 셋 = new ағын_мән(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 қабылдамау_мән"); }
        System.out.println("ағын_мән 완료");
    }
}
