// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ikinyarwanda.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 inikode_agaciro 코드 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String Ibirimo_agaciro) { return Ibirimo_agaciro.getBytes(StandardCharsets.UTF_8); }
    public static String gusobanura_amakurushingiro(byte[] Ibirimo_agaciro) { return new String(Ibirimo_agaciro, StandardCharsets.UTF_8); }
    public static String kuboneza_agaciro(String Ibirimo_agaciro) { return Normalizer.normalize(Ibirimo_agaciro, Normalizer.Form.NFC); }
    public static int 코드포인트수(String Ibirimo_agaciro) { return Ibirimo_agaciro.codePointCount(0, Ibirimo_agaciro.length()); }
    public static List<String> 낱말(String Ibirimo_agaciro, Locale Ururimi) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Ururimi);
        나누개.setText(Ibirimo_agaciro);
        List<String> 결과 = new ArrayList<>();
        int ihuriro = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; ihuriro = 끝, 끝 = 나누개.next())
            결과.add(Ibirimo_agaciro.substring(ihuriro, 끝));
        return 결과;
    }
}
