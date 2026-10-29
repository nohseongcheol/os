// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Isi_Zulu.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 IYunikhodi_inani 코드 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String Okuqukethwe_inani) { return Okuqukethwe_inani.getBytes(StandardCharsets.UTF_8); }
    public static String guqulela_imininingwane(byte[] Okuqukethwe_inani) { return new String(Okuqukethwe_inani, StandardCharsets.UTF_8); }
    public static String beka_kujwayeleke_inani(String Okuqukethwe_inani) { return Normalizer.normalize(Okuqukethwe_inani, Normalizer.Form.NFC); }
    public static int 코드포인트수(String Okuqukethwe_inani) { return Okuqukethwe_inani.codePointCount(0, Okuqukethwe_inani.length()); }
    public static List<String> 낱말(String Okuqukethwe_inani, Locale Ulimi) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Ulimi);
        나누개.setText(Okuqukethwe_inani);
        List<String> 결과 = new ArrayList<>();
        int Sebenzisa = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; Sebenzisa = 끝, 끝 = 나누개.next())
            결과.add(Okuqukethwe_inani.substring(Sebenzisa, 끝));
        return 결과;
    }
}
