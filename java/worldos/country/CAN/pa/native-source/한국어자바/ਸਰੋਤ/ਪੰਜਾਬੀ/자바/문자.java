// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ਪੰਜਾਬੀ.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 ਯੂਨੀਕੋਡ_ਕੀਮਤ 코드 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String ਤਤਕਰਾ_ਕੀਮਤ) { return ਤਤਕਰਾ_ਕੀਮਤ.getBytes(StandardCharsets.UTF_8); }
    public static String ਬਦਲਾਵ_ਕਰੋ_ਸਮੱਗਰੀ(byte[] ਤਤਕਰਾ_ਕੀਮਤ) { return new String(ਤਤਕਰਾ_ਕੀਮਤ, StandardCharsets.UTF_8); }
    public static String ਸਧਾਰਨ_ਬਨਾਉਣਾ_ਕੀਮਤ(String ਤਤਕਰਾ_ਕੀਮਤ) { return Normalizer.normalize(ਤਤਕਰਾ_ਕੀਮਤ, Normalizer.Form.NFC); }
    public static int 코드포인트수(String ਤਤਕਰਾ_ਕੀਮਤ) { return ਤਤਕਰਾ_ਕੀਮਤ.codePointCount(0, ਤਤਕਰਾ_ਕੀਮਤ.length()); }
    public static List<String> 낱말(String ਤਤਕਰਾ_ਕੀਮਤ, Locale ਭਾਸ਼ਾ) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(ਭਾਸ਼ਾ);
        나누개.setText(ਤਤਕਰਾ_ਕੀਮਤ);
        List<String> ਮਾਪ = new ArrayList<>();
        int ਚਲਾਓ_2 = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; ਚਲਾਓ_2 = 끝, 끝 = 나누개.next())
            ਮਾਪ.add(ਤਤਕਰਾ_ਕੀਮਤ.substring(ਚਲਾਓ_2, 끝));
        return ਮਾਪ;
    }
}
