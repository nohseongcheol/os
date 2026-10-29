// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Монгол.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 юникод_утга 코드 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String Агуулга_утга) { return Агуулга_утга.getBytes(StandardCharsets.UTF_8); }
    public static String шифрийг_задлах_өгөгдөл(byte[] Агуулга_утга) { return new String(Агуулга_утга, StandardCharsets.UTF_8); }
    public static String нормчлох_утга(String Агуулга_утга) { return Normalizer.normalize(Агуулга_утга, Normalizer.Form.NFC); }
    public static int 코드포인트수(String Агуулга_утга) { return Агуулга_утга.codePointCount(0, Агуулга_утга.length()); }
    public static List<String> 낱말(String Агуулга_утга, Locale Хэл) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Хэл);
        나누개.setText(Агуулга_утга);
        List<String> 결과 = new ArrayList<>();
        int Ажиллуулах = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; Ажиллуулах = 끝, 끝 = 나누개.next())
            결과.add(Агуулга_утга.substring(Ажиллуулах, 끝));
        return 결과;
    }
}
