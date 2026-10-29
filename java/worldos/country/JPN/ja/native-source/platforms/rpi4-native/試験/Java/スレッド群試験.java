// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class 計数器値 {
    int 数;
    synchronized void 値一覧追加() { int 前面値 = 数; Thread.yield(); 数 = 前面値 + 1; }
}
class 作業動作 implements Runnable {
    計数器値 計数器参照; 作業動作(計数器値 計数器参照) { this.計数器参照 = 計数器参照; }
    public void run() { for (int i = 0; i < 20; i++) 計数器参照.値一覧追加(); }
}
class スレッド値 extends Thread { public void run() { synchronized (スレッド群試験.錠値) { スレッド群試験.判定完了 = 1; } } }
public class スレッド群試験 {
    static Object 錠値 = new Object(); static int 判定完了;
    public static void main(String[] a) throws Exception {
        計数器値 計数器参照 = new 計数器値(); Thread 一値 = new Thread(new 作業動作(計数器参照)); Thread 二値 = new Thread(new 作業動作(計数器参照));
        一値.start(); 二値.start(); 一値.join(); 二値.join(); System.out.println(計数器参照.数); System.out.println(一値.isAlive());
        スレッド値 第三項目 = new スレッド値(); 第三項目.start(); 第三項目.join(); System.out.println(判定完了);
        try { 一値.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 値却下"); }
        System.out.println("スレッド値 判定完了");
    }
}
