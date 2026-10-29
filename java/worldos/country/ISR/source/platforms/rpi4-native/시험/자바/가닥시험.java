// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class מונה_ערך {
    int 수;
    synchronized void 더하기() { int מצלמה_קדמית_ערך_ec1a6b96 = 수; Thread.yield(); 수 = מצלמה_קדמית_ערך_ec1a6b96 + 1; }
}
class משימה_המלצה implements Runnable {
    מונה_ערך מונה_הפנה; משימה_המלצה(מונה_ערך מונה_הפנה) { this.מונה_הפנה = מונה_הפנה; }
    public void run() { for (int i = 0; i < 20; i++) מונה_הפנה.더하기(); }
}
class שרשור_ערך extends Thread { public void run() { synchronized (가닥시험.נעל_ערך) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object נעל_ערך = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        מונה_ערך מונה_הפנה = new מונה_ערך(); Thread 하나 = new Thread(new משימה_המלצה(מונה_הפנה)); Thread 둘 = new Thread(new משימה_המלצה(מונה_הפנה));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(מונה_הפנה.수); System.out.println(하나.isAlive());
        שרשור_ערך 셋 = new שרשור_ערך(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 דחייה_ערך"); }
        System.out.println("שרשור_ערך 완료");
    }
}
