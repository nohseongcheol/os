// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Indonesia.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 UNICODE_VALUE CODE_VALUE 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String Isi_VALUE) { return Isi_VALUE.getBytes(StandardCharsets.UTF_8); }
    public static String dekripsikan_data(byte[] Isi_VALUE) { return new String(Isi_VALUE, StandardCharsets.UTF_8); }
    public static String normalkan_VALUE(String Isi_VALUE) { return Normalizer.normalize(Isi_VALUE, Normalizer.Form.NFC); }
    public static int poin_kode_COUNT(String Isi_VALUE) { return Isi_VALUE.codePointCount(0, Isi_VALUE.length()); }
    public static List<String> 낱말(String Isi_VALUE, Locale Bahasa) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Bahasa);
        나누개.setText(Isi_VALUE);
        List<String> hasil = new ArrayList<>();
        int jalankan = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; jalankan = 끝, 끝 = 나누개.next())
            hasil.add(Isi_VALUE.substring(jalankan, 끝));
        return hasil;
    }
}
