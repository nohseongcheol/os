// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Galego.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 UNICODE_VALOR CÓDIGO_VALOR 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String Contido_VALOR) { return Contido_VALOR.getBytes(StandardCharsets.UTF_8); }
    public static String descifrar_datos(byte[] Contido_VALOR) { return new String(Contido_VALOR, StandardCharsets.UTF_8); }
    public static String organizar_VALOR(String Contido_VALOR) { return Normalizer.normalize(Contido_VALOR, Normalizer.Form.NFC); }
    public static int código_de_carácter_CONTAR(String Contido_VALOR) { return Contido_VALOR.codePointCount(0, Contido_VALOR.length()); }
    public static List<String> 낱말(String Contido_VALOR, Locale Idioma) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Idioma);
        나누개.setText(Contido_VALOR);
        List<String> RESULTANTE = new ArrayList<>();
        int Executar_2 = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; Executar_2 = 끝, 끝 = 나누개.next())
            RESULTANTE.add(Contido_VALOR.substring(Executar_2, 끝));
        return RESULTANTE;
    }
}
