// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 Unicode_atuutilik 코드 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String Ilulingit_atuutilik) { return Ilulingit_atuutilik.getBytes(StandardCharsets.UTF_8); }
    public static String suqquinarunniirlit_titiqqat(byte[] Ilulingit_atuutilik) { return new String(Ilulingit_atuutilik, StandardCharsets.UTF_8); }
    public static String naammasitilli_atuutilik(String Ilulingit_atuutilik) { return Normalizer.normalize(Ilulingit_atuutilik, Normalizer.Form.NFC); }
    public static int 코드포인트수(String Ilulingit_atuutilik) { return Ilulingit_atuutilik.codePointCount(0, Ilulingit_atuutilik.length()); }
    public static List<String> 낱말(String Ilulingit_atuutilik, Locale pilirijjutinut_uqausiq) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(pilirijjutinut_uqausiq);
        나누개.setText(Ilulingit_atuutilik);
        List<String> 결과 = new ArrayList<>();
        int 시작 = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; 시작 = 끝, 끝 = 나누개.next())
            결과.add(Ilulingit_atuutilik.substring(시작, 끝));
        return 결과;
    }
}
