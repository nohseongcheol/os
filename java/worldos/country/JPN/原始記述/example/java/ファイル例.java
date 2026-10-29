// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class ファイル例 {
    public static void 起動処理() throws 日本語.内蔵.入力出力例外 {
        日本語.内蔵.ファイル.書込("java.txt", "JAVA ファイル: 日本語 😀\n");
        日本語.内蔵.出力.書込(日本語.内蔵.ファイル.読取("java.txt"));
    }
}
