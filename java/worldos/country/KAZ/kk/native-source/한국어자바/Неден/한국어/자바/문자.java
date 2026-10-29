// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 Юникод_мән код_мән 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String мазмұн_мән) { return мазмұн_мән.getBytes(StandardCharsets.UTF_8); }
    public static String шифрді_шешу_деректер(byte[] мазмұн_мән) { return new String(мазмұн_мән, StandardCharsets.UTF_8); }
    public static String нормалдау_мән(String мазмұн_мән) { return Normalizer.normalize(мазмұн_мән, Normalizer.Form.NFC); }
    public static int 코드포인트수(String мазмұн_мән) { return мазмұн_мән.codePointCount(0, мазмұн_мән.length()); }
    public static List<String> 낱말(String мазмұн_мән, Locale Тіл) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Тіл);
        나누개.setText(мазмұн_мән);
        List<String> НӘТИЖЕ = new ArrayList<>();
        int Орындау_2 = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; Орындау_2 = 끝, 끝 = 나누개.next())
            НӘТИЖЕ.add(мазмұн_мән.substring(Орындау_2, 끝));
        return НӘТИЖЕ;
    }
}
