// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 日本語.内蔵;

/** 日本語 API で宣言、送出、捕捉できる例外 空参照参照例外。 */
public class 空参照参照例外 extends java.lang.NullPointerException {
    public 空参照参照例外() { super(); }
    public 空参照参照例外(String 説明) { super(説明); }
    public String 説明() { return getMessage(); }
}
