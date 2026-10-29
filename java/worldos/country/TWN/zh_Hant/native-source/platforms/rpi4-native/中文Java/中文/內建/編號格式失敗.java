// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.內建;

/** 可透過中文 API 宣告、拋出和捕捉的例外：編號格式失敗。 */
public class 編號格式失敗 extends 無效實際參數異常 {
    public 編號格式失敗() { super(); }
    public 編號格式失敗(String 說明) { super(說明); }
    public String 說明() { return getMessage(); }
}
