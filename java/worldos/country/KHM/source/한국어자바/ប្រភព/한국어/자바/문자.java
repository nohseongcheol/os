// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 យូនីកូដ_តំលៃ កូដ_តំលៃ 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String មាតិកា_តំលៃ) { return មាតិកា_តំលៃ.getBytes(StandardCharsets.UTF_8); }
    public static String ដោះកូដ_ទិន្នន័យ(byte[] មាតិកា_តំលៃ) { return new String(មាតិកា_តំលៃ, StandardCharsets.UTF_8); }
    public static String ធ្វើអោយប្រក្រតី_តំលៃ(String មាតិកា_តំលៃ) { return Normalizer.normalize(មាតិកា_តំលៃ, Normalizer.Form.NFC); }
    public static int 코드포인트수(String មាតិកា_តំលៃ) { return មាតិកា_តំលៃ.codePointCount(0, មាតិកា_តំលៃ.length()); }
    public static List<String> 낱말(String មាតិកា_តំលៃ, Locale ភាសា) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(ភាសា);
        나누개.setText(មាតិកា_តំលៃ);
        List<String> ការវាស់វែង = new ArrayList<>();
        int រត់ = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; រត់ = 끝, 끝 = 나누개.next())
            ការវាស់វែង.add(មាតិកា_តំលៃ.substring(រត់, 끝));
        return ការវាស់វែង;
    }
}
