// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.內建;

/** 可透過中文 API 宣告、拋出和捕捉的例外：邊界異常。 */
public class 邊界異常 extends java.lang.IndexOutOfBoundsException {
    public 邊界異常() { super(); }
    public 邊界異常(String 說明) { super(說明); }
    public String 說明() { return getMessage(); }
}
