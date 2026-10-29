// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 色 {
    public static void main(String[] 引数) throws Exception {
        int 総和値 = 0;
        int 数 = 1;
        while (数 <= 10) {
            総和値 = 総和値 + 数;
            数 = 数 + 1;
        }
        日本語.内蔵.出力.番号書込(総和値);
        日本語.内蔵.ファイル.書込("aot.txt", "한글 AOT ファイル 😀");
        日本語.内蔵.出力.行書込(日本語.内蔵.ファイル.読取("aot.txt"));
    }
}
