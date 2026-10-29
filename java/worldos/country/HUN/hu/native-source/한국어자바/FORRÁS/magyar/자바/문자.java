// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package magyar.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 UNICODE_ÉRTÉK KÓD_ÉRTÉK 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] kódolás(String Tartalom_ÉRTÉK) { return Tartalom_ÉRTÉK.getBytes(StandardCharsets.UTF_8); }
    public static String visszafejt_adat(byte[] Tartalom_ÉRTÉK) { return new String(Tartalom_ÉRTÉK, StandardCharsets.UTF_8); }
    public static String normalizál_ÉRTÉK(String Tartalom_ÉRTÉK) { return Normalizer.normalize(Tartalom_ÉRTÉK, Normalizer.Form.NFC); }
    public static int kódpont_DARAB(String Tartalom_ÉRTÉK) { return Tartalom_ÉRTÉK.codePointCount(0, Tartalom_ÉRTÉK.length()); }
    public static List<String> 낱말(String Tartalom_ÉRTÉK, Locale Nyelv) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Nyelv);
        나누개.setText(Tartalom_ÉRTÉK);
        List<String> KR = new ArrayList<>();
        int Futtatás = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; Futtatás = 끝, 끝 = 나누개.next())
            KR.add(Tartalom_ÉRTÉK.substring(Futtatás, 끝));
        return KR;
    }
}
