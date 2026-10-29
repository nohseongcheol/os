// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Македонски.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 UNICODE_VALUE CODE_VALUE 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String Содржина_VALUE) { return Содржина_VALUE.getBytes(StandardCharsets.UTF_8); }
    public static String дешифрирај_податоци(byte[] Содржина_VALUE) { return new String(Содржина_VALUE, StandardCharsets.UTF_8); }
    public static String нормализирање_VALUE(String Содржина_VALUE) { return Normalizer.normalize(Содржина_VALUE, Normalizer.Form.NFC); }
    public static int кодна_точка_COUNT(String Содржина_VALUE) { return Содржина_VALUE.codePointCount(0, Содржина_VALUE.length()); }
    public static List<String> 낱말(String Содржина_VALUE, Locale јазик) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(јазик);
        나누개.setText(Содржина_VALUE);
        List<String> мерка = new ArrayList<>();
        int Изврши_2 = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; Изврши_2 = 끝, 끝 = 나누개.next())
            мерка.add(Содржина_VALUE.substring(Изврши_2, 끝));
        return мерка;
    }
}
