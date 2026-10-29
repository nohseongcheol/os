// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.内置;
/** 把待执行任务交给自研界面的事件队列。 */
public final class 事件排队 {
    private 事件排队() {}
    public static native void 调用稍后(可运行任务任务 任务动作);
    public static native boolean 是否事件分派中();
}
