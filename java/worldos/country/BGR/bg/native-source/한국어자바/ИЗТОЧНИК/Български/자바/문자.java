// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Български.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 유니코드 код_стойност 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] кодирам(String Съдържание_стойност) { return Съдържание_стойност.getBytes(StandardCharsets.UTF_8); }
    public static String дешифрирам_данни(byte[] Съдържание_стойност) { return new String(Съдържание_стойност, StandardCharsets.UTF_8); }
    public static String нормализирам_стойност(String Съдържание_стойност) { return Normalizer.normalize(Съдържание_стойност, Normalizer.Form.NFC); }
    public static int 코드포인트수(String Съдържание_стойност) { return Съдържание_стойност.codePointCount(0, Съдържание_стойност.length()); }
    public static List<String> 낱말(String Съдържание_стойност, Locale език) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(език);
        나누개.setText(Съдържание_стойност);
        List<String> РЕЗУЛТАТ = new ArrayList<>();
        int Стартиране = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; Стартиране = 끝, 끝 = 나누개.next())
            РЕЗУЛТАТ.add(Съдържание_стойност.substring(Стартиране, 끝));
        return РЕЗУЛТАТ;
    }
}
