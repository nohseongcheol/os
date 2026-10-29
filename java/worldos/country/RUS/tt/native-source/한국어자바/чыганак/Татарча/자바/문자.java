// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Татарча.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 Юникод_VALUE CODE_VALUE 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String Эчтәлек_VALUE) { return Эчтәлек_VALUE.getBytes(StandardCharsets.UTF_8); }
    public static String шифрны_ачу_мәгълүмат(byte[] Эчтәлек_VALUE) { return new String(Эчтәлек_VALUE, StandardCharsets.UTF_8); }
    public static String нормальләштерү_VALUE(String Эчтәлек_VALUE) { return Normalizer.normalize(Эчтәлек_VALUE, Normalizer.Form.NFC); }
    public static int символ_коды_COUNT(String Эчтәлек_VALUE) { return Эчтәлек_VALUE.codePointCount(0, Эчтәлек_VALUE.length()); }
    public static List<String> 낱말(String Эчтәлек_VALUE, Locale тел) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(тел);
        나누개.setText(Эчтәлек_VALUE);
        List<String> үлчәм = new ArrayList<>();
        int эшләтү = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; эшләтү = 끝, 끝 = 나누개.next())
            үлчәм.add(Эчтәлек_VALUE.substring(эшләтү, 끝));
        return үлчәм;
    }
}
