// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 中文.內建.字元;
import 中文.內建.檔案;
import 中文.內建.條目列表;
import 中文.內建.字典;
import 中文.內建.輸出;
public class 測試韓文字母 {
    public static void main(String[] a) throws Exception {
        String 問候例 = "안녕하세요 · 日本語 · العربية · 😀";
        輸出.寫入行(字元.解密資料(字元.編碼(問候例))); 輸出.寫入編號(字元.程式碼分個數("한글😀"));
        檔案.寫入("한글자료.txt", 問候例); 輸出.寫入行(檔案.讀取("한글자료.txt"));
        條目列表 名稱列列表 = new 條目列表(); 名稱列列表.添加值列("가람"); 名稱列列表.添加值列("누리"); 輸出.寫入行(名稱列列表.讀取(1));
        字典 含義值 = new 字典(); 含義值.放入值("가람", "강"); System.gc(); 輸出.寫入行(含義值.查找條目("가람"));
        try { 字元.解密資料(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { 輸出.寫入行("UTF-8 錯誤 拒絕值"); }
        輸出.寫入行("中文 庫 是否完成");
    }
}
