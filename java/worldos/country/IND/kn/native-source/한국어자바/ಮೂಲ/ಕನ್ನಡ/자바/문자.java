// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ಕನ್ನಡ.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 ಯುನಿಕೋಡ್_ಮೌಲ್ಯ ಕೋಡ್_ಮೌಲ್ಯ 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String ವಿಷಯ_ಮೌಲ್ಯ) { return ವಿಷಯ_ಮೌಲ್ಯ.getBytes(StandardCharsets.UTF_8); }
    public static String ಡೀಕ್ರಿಪ್ಟ್_ಮಾಡಿ_ಡೇಟಾ(byte[] ವಿಷಯ_ಮೌಲ್ಯ) { return new String(ವಿಷಯ_ಮೌಲ್ಯ, StandardCharsets.UTF_8); }
    public static String ಸಮಾನೀಕರಿಸು_ಮೌಲ್ಯ(String ವಿಷಯ_ಮೌಲ್ಯ) { return Normalizer.normalize(ವಿಷಯ_ಮೌಲ್ಯ, Normalizer.Form.NFC); }
    public static int 코드포인트수(String ವಿಷಯ_ಮೌಲ್ಯ) { return ವಿಷಯ_ಮೌಲ್ಯ.codePointCount(0, ವಿಷಯ_ಮೌಲ್ಯ.length()); }
    public static List<String> 낱말(String ವಿಷಯ_ಮೌಲ್ಯ, Locale ಭಾಷೆ) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(ಭಾಷೆ);
        나누개.setText(ವಿಷಯ_ಮೌಲ್ಯ);
        List<String> ಮಾಪನ = new ArrayList<>();
        int ಚಲಾಯಿಸು_2 = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; ಚಲಾಯಿಸು_2 = 끝, 끝 = 나누개.next())
            ಮಾಪನ.add(ವಿಷಯ_ಮೌಲ್ಯ.substring(ಚಲಾಯಿಸು_2, 끝));
        return ಮಾಪನ;
    }
}
