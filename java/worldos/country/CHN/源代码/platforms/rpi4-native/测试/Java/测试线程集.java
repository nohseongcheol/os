// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class 计数器值 {
    int 数;
    synchronized void 添加值列() { int 前端值 = 数; Thread.yield(); 数 = 前端值 + 1; }
}
class 任务动作 implements Runnable {
    计数器值 计数器引用; 任务动作(计数器值 计数器引用) { this.计数器引用 = 计数器引用; }
    public void run() { for (int i = 0; i < 20; i++) 计数器引用.添加值列(); }
}
class 线程值 extends Thread { public void run() { synchronized (测试线程集.锁值) { 测试线程集.是否完成 = 1; } } }
public class 测试线程集 {
    static Object 锁值 = new Object(); static int 是否完成;
    public static void main(String[] a) throws Exception {
        计数器值 计数器引用 = new 计数器值(); Thread 一值 = new Thread(new 任务动作(计数器引用)); Thread 二值 = new Thread(new 任务动作(计数器引用));
        一值.start(); 二值.start(); 一值.join(); 二值.join(); System.out.println(计数器引用.数); System.out.println(一值.isAlive());
        线程值 第三项目 = new 线程值(); 第三项目.start(); 第三项目.join(); System.out.println(是否完成);
        try { 一值.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 拒绝值"); }
        System.out.println("线程值 是否完成");
    }
}
