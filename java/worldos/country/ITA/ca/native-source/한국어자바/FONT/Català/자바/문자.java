// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Català.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 UNICODE_VALOR CODI_VALOR 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String contingut_VALOR) { return contingut_VALOR.getBytes(StandardCharsets.UTF_8); }
    public static String desencriptar_dades(byte[] contingut_VALOR) { return new String(contingut_VALOR, StandardCharsets.UTF_8); }
    public static String normalitzar_VALOR(String contingut_VALOR) { return Normalizer.normalize(contingut_VALOR, Normalizer.Form.NFC); }
    public static int codi_de_caràcter_COMPT(String contingut_VALOR) { return contingut_VALOR.codePointCount(0, contingut_VALOR.length()); }
    public static List<String> 낱말(String contingut_VALOR, Locale Idioma) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Idioma);
        나누개.setText(contingut_VALOR);
        List<String> RESULTAT = new ArrayList<>();
        int Executa_2 = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; Executa_2 = 끝, 끝 = 나누개.next())
            RESULTAT.add(contingut_VALOR.substring(Executa_2, 끝));
        return RESULTAT;
    }
}
