// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 日本語.内蔵;

/** タスク自体の終了ではなく、スレッドを待つ操作の中断を表す。 */
public class 待合中断済み例外 extends java.lang.InterruptedException {
    public 待合中断済み例外() { super(); }
    public 待合中断済み例外(String 説明) { super(説明); }
    public String 説明() { return getMessage(); }
}
