// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class ハングルソース {
    public static void main(String[] 引数) throws 日本語.内蔵.入力出力例外 {
        日本語.内蔵.出力.行書込("内蔵 컴파일러와 日本語 ライブラリ");
        int 文字個数 = 日本語.内蔵.文字.コード点個数("한글😀");
        日本語.内蔵.出力.番号書込(文字個数);
        日本語.内蔵.ファイル.書込("한글자료.txt", "内蔵 中核値 안에서 저장한 한글😀");
        日本語.内蔵.出力.行書込(日本語.内蔵.ファイル.読取("한글자료.txt"));
    }
}
