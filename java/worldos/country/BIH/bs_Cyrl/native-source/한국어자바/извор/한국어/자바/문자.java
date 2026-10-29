// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 Unicode_вриједност 코드 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String Садржај_вриједност) { return Садржај_вриједност.getBytes(StandardCharsets.UTF_8); }
    public static String дешифрирати_подаци(byte[] Садржај_вриједност) { return new String(Садржај_вриједност, StandardCharsets.UTF_8); }
    public static String нормализирати_вриједност(String Садржај_вриједност) { return Normalizer.normalize(Садржај_вриједност, Normalizer.Form.NFC); }
    public static int 코드포인트수(String Садржај_вриједност) { return Садржај_вриједност.codePointCount(0, Садржај_вриједност.length()); }
    public static List<String> 낱말(String Садржај_вриједност, Locale Језик) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Језик);
        나누개.setText(Садржај_вриједност);
        List<String> 결과 = new ArrayList<>();
        int 시작 = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; 시작 = 끝, 끝 = 나누개.next())
            결과.add(Садржај_вриједност.substring(시작, 끝));
        return 결과;
    }
}
