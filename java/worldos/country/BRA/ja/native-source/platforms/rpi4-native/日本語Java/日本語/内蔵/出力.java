// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 日本語.内蔵;
/** 独自カーネルの標準出力。UTF-16 のサロゲート対を UART から UTF-8 で送る。 */
public final class 出力 {
    private 出力() {}
    public static void 書込(String 文) { System.out.print(文); }
    public static void 行書込(String 文) { System.out.println(文); }
    public static void 番号書込(int 数) { System.out.println(数); }
}
