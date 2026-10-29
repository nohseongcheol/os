// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.Java;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class 任务 {
    private 任务() {}
    public static Thread 运行(String 名称, Runnable 动作) {
        Thread 线程值 = new Thread(动作, 名称);
        线程值.start();
        return 线程值;
    }
    public static void 等待(Thread 线程值) throws InterruptedException { 线程值.join(); }
    public static void 剩余部分短暂地(long 毫秒) throws InterruptedException { Thread.sleep(毫秒); }
    /** 调用者必须通过 shutdown() 释放资源。 */
    public static ExecutorService 工作台值(int 线程个数) { return Executors.newFixedThreadPool(线程个数); }
}
