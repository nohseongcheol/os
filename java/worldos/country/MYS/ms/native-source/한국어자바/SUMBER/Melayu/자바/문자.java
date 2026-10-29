// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Melayu.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 Unikod_VALUE kod_VALUE 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String Kandungan_VALUE) { return Kandungan_VALUE.getBytes(StandardCharsets.UTF_8); }
    public static String nyahsulit_data(byte[] Kandungan_VALUE) { return new String(Kandungan_VALUE, StandardCharsets.UTF_8); }
    public static String menormalkan_VALUE(String Kandungan_VALUE) { return Normalizer.normalize(Kandungan_VALUE, Normalizer.Form.NFC); }
    public static int titik_kod_COUNT(String Kandungan_VALUE) { return Kandungan_VALUE.codePointCount(0, Kandungan_VALUE.length()); }
    public static List<String> 낱말(String Kandungan_VALUE, Locale Bahasa) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Bahasa);
        나누개.setText(Kandungan_VALUE);
        List<String> ukuran = new ArrayList<>();
        int Jalan = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; Jalan = 끝, 끝 = 나누개.next())
            ukuran.add(Kandungan_VALUE.substring(Jalan, 끝));
        return ukuran;
    }
}
