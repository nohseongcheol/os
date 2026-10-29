// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.内置;
/** 由自研 JVM 调度器管理的执行流，不包装标准 Thread。 */
public final class 后台任务 {
    public 后台任务(可运行任务任务 任务动作) {
        throw new 状态异常("自有 JVM 需要支持创建中文 API 线程。");
    }
    public native void 开始任务() throws 线程状态异常;
    public native void 等待() throws 等待状态已中断异常;
    public native boolean 是否存活();
    public static native void 挂起任务();
}
