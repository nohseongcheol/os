// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class 計數器值 {
    int 數;
    synchronized void 添加值列() { int 前端值 = 數; Thread.yield(); 數 = 前端值 + 1; }
}
class 任務動作 implements Runnable {
    計數器值 計數器引用; 任務動作(計數器值 計數器引用) { this.計數器引用 = 計數器引用; }
    public void run() { for (int i = 0; i < 20; i++) 計數器引用.添加值列(); }
}
class 執行緒值 extends Thread { public void run() { synchronized (測試執行緒集.鎖值) { 測試執行緒集.是否完成 = 1; } } }
public class 測試執行緒集 {
    static Object 鎖值 = new Object(); static int 是否完成;
    public static void main(String[] a) throws Exception {
        計數器值 計數器引用 = new 計數器值(); Thread 一值 = new Thread(new 任務動作(計數器引用)); Thread 二值 = new Thread(new 任務動作(計數器引用));
        一值.start(); 二值.start(); 一值.join(); 二值.join(); System.out.println(計數器引用.數); System.out.println(一值.isAlive());
        執行緒值 第三項目 = new 執行緒值(); 第三項目.start(); 第三項目.join(); System.out.println(是否完成);
        try { 一值.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 拒絕值"); }
        System.out.println("執行緒值 是否完成");
    }
}
