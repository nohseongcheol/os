// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.内置;

/** 表示等待线程的操作被中断，而不是任务本身结束。 */
public class 等待状态已中断异常 extends java.lang.InterruptedException {
    public 等待状态已中断异常() { super(); }
    public 等待状态已中断异常(String 说明) { super(说明); }
    public String 说明() { return getMessage(); }
}
