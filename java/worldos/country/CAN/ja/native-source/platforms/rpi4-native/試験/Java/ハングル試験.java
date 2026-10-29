// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 日本語.内蔵.文字;
import 日本語.内蔵.ファイル;
import 日本語.内蔵.入口一覧;
import 日本語.内蔵.辞書;
import 日本語.内蔵.出力;
public class ハングル試験 {
    public static void main(String[] a) throws Exception {
        String 挨拶例 = "안녕하세요 · 日本語 · العربية · 😀";
        出力.行書込(文字.データ復号化(文字.符号化(挨拶例))); 出力.番号書込(文字.コード点個数("한글😀"));
        ファイル.書込("한글자료.txt", 挨拶例); 出力.行書込(ファイル.読取("한글자료.txt"));
        入口一覧 名前一覧一覧 = new 入口一覧(); 名前一覧一覧.値一覧追加("가람"); 名前一覧一覧.値一覧追加("누리"); 出力.行書込(名前一覧一覧.読取(1));
        辞書 意味値 = new 辞書(); 意味値.値格納("가람", "강"); System.gc(); 出力.行書込(意味値.入口探索("가람"));
        try { 文字.データ復号化(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { 出力.行書込("UTF-8 エラー 値却下"); }
        出力.行書込("日本語 ライブラリ 判定完了");
    }
}
