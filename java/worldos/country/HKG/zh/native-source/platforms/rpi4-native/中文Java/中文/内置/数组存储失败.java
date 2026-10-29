// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.内置;

/** 可通过中文 API 声明、抛出和捕获的异常：数组存储失败。 */
public class 数组存储失败 extends java.lang.ArrayStoreException {
    public 数组存储失败() { super(); }
    public 数组存储失败(String 说明) { super(说明); }
    public String 说明() { return getMessage(); }
}
