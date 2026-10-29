// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.Java;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** 區分 UTF-16 char 數與 Unicode 碼位數。 */
public final class 字元 {
    private 字元() {}
    public static byte[] 編碼(String 內容值) { return 內容值.getBytes(StandardCharsets.UTF_8); }
    public static String 解密資料(byte[] 內容值) { return new String(內容值, StandardCharsets.UTF_8); }
    public static String 正規化值(String 內容值) { return Normalizer.normalize(內容值, Normalizer.Form.NFC); }
    public static int 程式碼分個數(String 內容值) { return 內容值.codePointCount(0, 內容值.length()); }
    public static List<String> 詞法用機器字(String 內容值, Locale 語言) {
        BreakIterator 除數值 = BreakIterator.getWordInstance(語言);
        除數值.setText(內容值);
        List<String> 結果 = new ArrayList<>();
        int 運行 = 除數值.first();
        for (int 結尾 = 除數值.next(); 結尾 != BreakIterator.DONE; 運行 = 結尾, 結尾 = 除數值.next())
            結果.add(內容值.substring(運行, 結尾));
        return 結果;
    }
}
