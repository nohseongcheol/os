// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Cymraeg.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 UNICODE_VALUE cod_VALUE 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String Cynnwys_VALUE) { return Cynnwys_VALUE.getBytes(StandardCharsets.UTF_8); }
    public static String dadgryptio_data(byte[] Cynnwys_VALUE) { return new String(Cynnwys_VALUE, StandardCharsets.UTF_8); }
    public static String normaleiddio_VALUE(String Cynnwys_VALUE) { return Normalizer.normalize(Cynnwys_VALUE, Normalizer.Form.NFC); }
    public static int cod_nod_COUNT(String Cynnwys_VALUE) { return Cynnwys_VALUE.codePointCount(0, Cynnwys_VALUE.length()); }
    public static List<String> 낱말(String Cynnwys_VALUE, Locale Iaith) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Iaith);
        나누개.setText(Cynnwys_VALUE);
        List<String> mesur = new ArrayList<>();
        int Gweithredu_2 = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; Gweithredu_2 = 끝, 끝 = 나누개.next())
            mesur.add(Cynnwys_VALUE.substring(Gweithredu_2, 끝));
        return mesur;
    }
}
