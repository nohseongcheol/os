// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Gaeilge.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 UNICODE_VALUE CODE_VALUE 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String Inneachar_VALUE) { return Inneachar_VALUE.getBytes(StandardCharsets.UTF_8); }
    public static String díchriptigh_sonraí(byte[] Inneachar_VALUE) { return new String(Inneachar_VALUE, StandardCharsets.UTF_8); }
    public static String normalaigh_VALUE(String Inneachar_VALUE) { return Normalizer.normalize(Inneachar_VALUE, Normalizer.Form.NFC); }
    public static int pointe_cóid_COUNT(String Inneachar_VALUE) { return Inneachar_VALUE.codePointCount(0, Inneachar_VALUE.length()); }
    public static List<String> 낱말(String Inneachar_VALUE, Locale Teanga) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Teanga);
        나누개.setText(Inneachar_VALUE);
        List<String> tomhas = new ArrayList<>();
        int Rith_2 = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; Rith_2 = 끝, 끝 = 나누개.next())
            tomhas.add(Inneachar_VALUE.substring(Rith_2, 끝));
        return tomhas;
    }
}
