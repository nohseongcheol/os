// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ગુજરાતી.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 યુનિકોડ_મૂલ્ય 코드 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String સામગ્રી_મૂલ્ય) { return સામગ્રી_મૂલ્ય.getBytes(StandardCharsets.UTF_8); }
    public static String ડિક્રિપ્ટ_કરો_ડેટા(byte[] સામગ્રી_મૂલ્ય) { return new String(સામગ્રી_મૂલ્ય, StandardCharsets.UTF_8); }
    public static String સામાન્ય_બનાવો_મૂલ્ય(String સામગ્રી_મૂલ્ય) { return Normalizer.normalize(સામગ્રી_મૂલ્ય, Normalizer.Form.NFC); }
    public static int 코드포인트수(String સામગ્રી_મૂલ્ય) { return સામગ્રી_મૂલ્ય.codePointCount(0, સામગ્રી_મૂલ્ય.length()); }
    public static List<String> 낱말(String સામગ્રી_મૂલ્ય, Locale ભાષા) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(ભાષા);
        나누개.setText(સામગ્રી_મૂલ્ય);
        List<String> પરિમાણ = new ArrayList<>();
        int ચલાવો_2 = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; ચલાવો_2 = 끝, 끝 = 나누개.next())
            પરિમાણ.add(સામગ્રી_મૂલ્ય.substring(ચલાવો_2, 끝));
        return પરિમાણ;
    }
}
