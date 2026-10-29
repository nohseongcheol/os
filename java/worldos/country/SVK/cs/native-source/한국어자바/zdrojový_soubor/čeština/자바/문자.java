// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package čeština.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 UNICODE_HODNOTA KÓD_HODNOTA 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] kódovat(String Obsah_HODNOTA) { return Obsah_HODNOTA.getBytes(StandardCharsets.UTF_8); }
    public static String dešifrovat_data(byte[] Obsah_HODNOTA) { return new String(Obsah_HODNOTA, StandardCharsets.UTF_8); }
    public static String normalizovat_HODNOTA(String Obsah_HODNOTA) { return Normalizer.normalize(Obsah_HODNOTA, Normalizer.Form.NFC); }
    public static int bod_kódu_POČET(String Obsah_HODNOTA) { return Obsah_HODNOTA.codePointCount(0, Obsah_HODNOTA.length()); }
    public static List<String> 낱말(String Obsah_HODNOTA, Locale Jazyk) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Jazyk);
        나누개.setText(Obsah_HODNOTA);
        List<String> VÝSLEDEK = new ArrayList<>();
        int Spustit_2 = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; Spustit_2 = 끝, 끝 = 나누개.next())
            VÝSLEDEK.add(Obsah_HODNOTA.substring(Spustit_2, 끝));
        return VÝSLEDEK;
    }
}
