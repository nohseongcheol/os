// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 日本語.内蔵;

/** 日本語 API で宣言、送出、捕捉できる例外 負数配列容量失敗。 */
public class 負数配列容量失敗 extends java.lang.NegativeArraySizeException {
    public 負数配列容量失敗() { super(); }
    public 負数配列容量失敗(String 説明) { super(説明); }
    public String 説明() { return getMessage(); }
}
