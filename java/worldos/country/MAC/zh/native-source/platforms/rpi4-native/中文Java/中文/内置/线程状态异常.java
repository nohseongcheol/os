// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.内置;

/** 可通过中文 API 声明、抛出和捕获的异常：线程状态异常。 */
public class 线程状态异常 extends java.lang.IllegalThreadStateException {
    public 线程状态异常() { super(); }
    public 线程状态异常(String 说明) { super(说明); }
    public String 说明() { return getMessage(); }
}
