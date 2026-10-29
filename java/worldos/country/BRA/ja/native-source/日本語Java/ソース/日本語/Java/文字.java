// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 日本語.Java;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 の char 数と Unicode 符号位置数を区別する。 */
public final class 文字 {
    private 文字() {}
    public static byte[] 符号化(String 内容物値) { return 内容物値.getBytes(StandardCharsets.UTF_8); }
    public static String データ復号化(byte[] 内容物値) { return new String(内容物値, StandardCharsets.UTF_8); }
    public static String 値正規化(String 内容物値) { return Normalizer.normalize(内容物値, Normalizer.Form.NFC); }
    public static int コード点個数(String 内容物値) { return 内容物値.codePointCount(0, 内容物値.length()); }
    public static List<String> 字句用語(String 内容物値, Locale 言語) {
        BreakIterator 除数値 = BreakIterator.getWordInstance(言語);
        除数値.setText(内容物値);
        List<String> 結果 = new ArrayList<>();
        int 起動処理 = 除数値.first();
        for (int 終端 = 除数値.next(); 終端 != BreakIterator.DONE; 起動処理 = 終端, 終端 = 除数値.next())
            結果.add(内容物値.substring(起動処理, 終端));
        return 結果;
    }
}
