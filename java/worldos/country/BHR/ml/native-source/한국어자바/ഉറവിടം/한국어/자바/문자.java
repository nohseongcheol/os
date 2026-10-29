// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 യൂണികോഡ്_മൂല്യം കോഡ്_മൂല്യം 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String ഉള്ളടക്കം_മൂല്യം) { return ഉള്ളടക്കം_മൂല്യം.getBytes(StandardCharsets.UTF_8); }
    public static String ഗൂഢഭാഷമാറ്റുക_ഡാറ്റാ(byte[] ഉള്ളടക്കം_മൂല്യം) { return new String(ഉള്ളടക്കം_മൂല്യം, StandardCharsets.UTF_8); }
    public static String ക്രമാനുസരണമാക്കുക_മൂല്യം(String ഉള്ളടക്കം_മൂല്യം) { return Normalizer.normalize(ഉള്ളടക്കം_മൂല്യം, Normalizer.Form.NFC); }
    public static int 코드포인트수(String ഉള്ളടക്കം_മൂല്യം) { return ഉള്ളടക്കം_മൂല്യം.codePointCount(0, ഉള്ളടക്കം_മൂല്യം.length()); }
    public static List<String> 낱말(String ഉള്ളടക്കം_മൂല്യം, Locale భాష) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(భాష);
        나누개.setText(ഉള്ളടക്കം_മൂല്യം);
        List<String> അളവ് = new ArrayList<>();
        int നടപ്പിലാക്കുക = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; നടപ്പിലാക്കുക = 끝, 끝 = 나누개.next())
            അളവ്.add(ഉള്ളടക്കം_മൂല്യം.substring(നടപ്പിലാക്കുക, 끝));
        return അളവ്;
    }
}
