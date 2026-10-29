// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.内置;
/** 线程是一条执行流；自研 JVM 根据已执行指令数交替运行各线程。 */
public final class 任务 {
    private 任务() {}
    public static 后台任务 运行(可运行任务任务 任务动作) { 后台任务 线程值 = new 后台任务(任务动作); 线程值.开始任务(); return 线程值; }
    public static void 等待(后台任务 线程值) throws 等待状态已中断异常 { 线程值.等待(); }
    public static boolean 是否存活(后台任务 线程值) { return 线程值.是否存活(); }
    public static void 挂起任务() { 后台任务.挂起任务(); }
}
