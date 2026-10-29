// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 Юникод_маани 코드 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String Мазмун_маани) { return Мазмун_маани.getBytes(StandardCharsets.UTF_8); }
    public static String чечмелөө_берилмелер(byte[] Мазмун_маани) { return new String(Мазмун_маани, StandardCharsets.UTF_8); }
    public static String нормалдаштыруу_маани(String Мазмун_маани) { return Normalizer.normalize(Мазмун_маани, Normalizer.Form.NFC); }
    public static int 코드포인트수(String Мазмун_маани) { return Мазмун_маани.codePointCount(0, Мазмун_маани.length()); }
    public static List<String> 낱말(String Мазмун_маани, Locale Тил) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Тил);
        나누개.setText(Мазмун_маани);
        List<String> 결과 = new ArrayList<>();
        int Жүргүзүү = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; Жүргүзүү = 끝, 끝 = 나누개.next())
            결과.add(Мазмун_маани.substring(Жүргүзүү, 끝));
        return 결과;
    }
}
