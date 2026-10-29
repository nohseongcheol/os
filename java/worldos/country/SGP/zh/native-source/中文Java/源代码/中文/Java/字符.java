// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.Java;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** 区分 UTF-16 char 数与 Unicode 码点数。 */
public final class 字符 {
    private 字符() {}
    public static byte[] 编码(String 内容值) { return 内容值.getBytes(StandardCharsets.UTF_8); }
    public static String 解密数据(byte[] 内容值) { return new String(内容值, StandardCharsets.UTF_8); }
    public static String 正规化值(String 内容值) { return Normalizer.normalize(内容值, Normalizer.Form.NFC); }
    public static int 代码分个数(String 内容值) { return 内容值.codePointCount(0, 内容值.length()); }
    public static List<String> 词法用机器字(String 内容值, Locale 语言) {
        BreakIterator 除数值 = BreakIterator.getWordInstance(语言);
        除数值.setText(内容值);
        List<String> 结果 = new ArrayList<>();
        int 运行 = 除数值.first();
        for (int 结尾 = 除数值.next(); 结尾 != BreakIterator.DONE; 运行 = 结尾, 结尾 = 除数值.next())
            结果.add(内容值.substring(运行, 结尾));
        return 结果;
    }
}
