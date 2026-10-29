// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.內建;
/** 獨立核心的標準輸出；UTF-16 代理對透過 UART 以 UTF-8 傳送。 */
public final class 輸出 {
    private 輸出() {}
    public static void 寫入(String 文本) { System.out.print(文本); }
    public static void 寫入行(String 文本) { System.out.println(文本); }
    public static void 寫入編號(int 數) { System.out.println(數); }
}
