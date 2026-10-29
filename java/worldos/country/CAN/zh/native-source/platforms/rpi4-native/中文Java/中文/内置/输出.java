// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.内置;
/** 独立内核的标准输出；UTF-16 代理对通过 UART 以 UTF-8 发送。 */
public final class 输出 {
    private 输出() {}
    public static void 写入(String 文本) { System.out.print(文本); }
    public static void 写入行(String 文本) { System.out.println(文本); }
    public static void 写入编号(int 数) { System.out.println(数); }
}
