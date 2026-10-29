// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 日本語.内蔵;

/** 日本語 API で宣言、送出、捕捉できる例外 番地検索例外。 */
public class 番地検索例外 extends 入力出力例外 {
    public 番地検索例外() { super(); }
    public 番地検索例外(String 説明) { super(説明); }
    public String 説明() { return getMessage(); }
}
