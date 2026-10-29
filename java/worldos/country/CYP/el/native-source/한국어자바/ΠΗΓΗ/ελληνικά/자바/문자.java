// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ελληνικά.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 유니코드 κωδικός_τιμή 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] κωδικοποιώ(String Περιεχόμενο_τιμή) { return Περιεχόμενο_τιμή.getBytes(StandardCharsets.UTF_8); }
    public static String αποκρυπτογραφώ_δεδομένα(byte[] Περιεχόμενο_τιμή) { return new String(Περιεχόμενο_τιμή, StandardCharsets.UTF_8); }
    public static String κανονικοποίηση_τιμή(String Περιεχόμενο_τιμή) { return Normalizer.normalize(Περιεχόμενο_τιμή, Normalizer.Form.NFC); }
    public static int 코드포인트수(String Περιεχόμενο_τιμή) { return Περιεχόμενο_τιμή.codePointCount(0, Περιεχόμενο_τιμή.length()); }
    public static List<String> 낱말(String Περιεχόμενο_τιμή, Locale Γλώσσα) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Γλώσσα);
        나누개.setText(Περιεχόμενο_τιμή);
        List<String> μέτρηση = new ArrayList<>();
        int Εκτέλεση_2 = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; Εκτέλεση_2 = 끝, 끝 = 나누개.next())
            μέτρηση.add(Περιεχόμενο_τιμή.substring(Εκτέλεση_2, 끝));
        return μέτρηση;
    }
}
