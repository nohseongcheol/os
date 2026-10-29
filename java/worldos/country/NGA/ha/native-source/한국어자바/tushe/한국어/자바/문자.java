// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 Ɗan_maƙalu_Daraja lambar_sirri_Daraja 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String kunshiya_Daraja) { return kunshiya_Daraja.getBytes(StandardCharsets.UTF_8); }
    public static String Bude_Tarin_bayani(byte[] kunshiya_Daraja) { return new String(kunshiya_Daraja, StandardCharsets.UTF_8); }
    public static String Gajarta_kimar_bayanai_Daraja(String kunshiya_Daraja) { return Normalizer.normalize(kunshiya_Daraja, Normalizer.Form.NFC); }
    public static int 코드포인트수(String kunshiya_Daraja) { return kunshiya_Daraja.codePointCount(0, kunshiya_Daraja.length()); }
    public static List<String> 낱말(String kunshiya_Daraja, Locale yare) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(yare);
        나누개.setText(kunshiya_Daraja);
        List<String> 결과 = new ArrayList<>();
        int Tafiyar_da = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; Tafiyar_da = 끝, 끝 = 나누개.next())
            결과.add(kunshiya_Daraja.substring(Tafiyar_da, 끝));
        return 결과;
    }
}
