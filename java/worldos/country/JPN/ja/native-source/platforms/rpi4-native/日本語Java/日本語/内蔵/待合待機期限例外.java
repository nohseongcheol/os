// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 日本語.内蔵;

/** 日本語 API で宣言、送出、捕捉できる例外 待合待機期限例外。 */
public class 待合待機期限例外 extends 入力出力例外 {
    public 待合待機期限例外() { super(); }
    public 待合待機期限例外(String 説明) { super(説明); }
    public String 説明() { return getMessage(); }
}
