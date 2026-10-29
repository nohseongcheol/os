// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package polski.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 UNICODE_WARTOŚĆ KOD_WARTOŚĆ 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] kodować(String treść_WARTOŚĆ_cb0f2404) { return treść_WARTOŚĆ_cb0f2404.getBytes(StandardCharsets.UTF_8); }
    public static String odszyfrować_dane(byte[] treść_WARTOŚĆ_cb0f2404) { return new String(treść_WARTOŚĆ_cb0f2404, StandardCharsets.UTF_8); }
    public static String normalizować_WARTOŚĆ(String treść_WARTOŚĆ_cb0f2404) { return Normalizer.normalize(treść_WARTOŚĆ_cb0f2404, Normalizer.Form.NFC); }
    public static int kod_znaku_ILE_LICZB(String treść_WARTOŚĆ_cb0f2404) { return treść_WARTOŚĆ_cb0f2404.codePointCount(0, treść_WARTOŚĆ_cb0f2404.length()); }
    public static List<String> 낱말(String treść_WARTOŚĆ_cb0f2404, Locale Język) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Język);
        나누개.setText(treść_WARTOŚĆ_cb0f2404);
        List<String> WYNIK = new ArrayList<>();
        int Uruchom_2 = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; Uruchom_2 = 끝, 끝 = 나누개.next())
            WYNIK.add(treść_WARTOŚĆ_cb0f2404.substring(Uruchom_2, 끝));
        return WYNIK;
    }
}
