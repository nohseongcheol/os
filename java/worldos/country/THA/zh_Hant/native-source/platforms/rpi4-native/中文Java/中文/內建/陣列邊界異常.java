// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.內建;

/** 可透過中文 API 宣告、拋出和捕捉的例外：陣列邊界異常。 */
public class 陣列邊界異常 extends 邊界異常 {
    public 陣列邊界異常() { super(); }
    public 陣列邊界異常(String 說明) { super(說明); }
    public String 說明() { return getMessage(); }
}
