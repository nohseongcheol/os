// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 Յունիկոդ_արժեք կոդ_արժեք 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String Բովանդակություն_արժեք) { return Բովանդակություն_արժեք.getBytes(StandardCharsets.UTF_8); }
    public static String վերծանել_տվյալ(byte[] Բովանդակություն_արժեք) { return new String(Բովանդակություն_արժեք, StandardCharsets.UTF_8); }
    public static String կարգավորել_արժեք(String Բովանդակություն_արժեք) { return Normalizer.normalize(Բովանդակություն_արժեք, Normalizer.Form.NFC); }
    public static int 코드포인트수(String Բովանդակություն_արժեք) { return Բովանդակություն_արժեք.codePointCount(0, Բովանդակություն_արժեք.length()); }
    public static List<String> 낱말(String Բովանդակություն_արժեք, Locale Լեզու) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Լեզու);
        나누개.setText(Բովանդակություն_արժեք);
        List<String> չափ = new ArrayList<>();
        int Գործարկել = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; Գործարկել = 끝, 끝 = 나누개.next())
            չափ.add(Բովանդակություն_արժեք.substring(Գործարկել, 끝));
        return չափ;
    }
}
