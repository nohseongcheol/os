// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Português.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 UNICODE_VALOR valor_do_código 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] codificar(String Conteúdo_VALOR) { return Conteúdo_VALOR.getBytes(StandardCharsets.UTF_8); }
    public static String descriptografar_dados(byte[] Conteúdo_VALOR) { return new String(Conteúdo_VALOR, StandardCharsets.UTF_8); }
    public static String normalizar_VALOR(String Conteúdo_VALOR) { return Normalizer.normalize(Conteúdo_VALOR, Normalizer.Form.NFC); }
    public static int ponto_de_código_CONT_NÚM(String Conteúdo_VALOR) { return Conteúdo_VALOR.codePointCount(0, Conteúdo_VALOR.length()); }
    public static List<String> 낱말(String Conteúdo_VALOR, Locale Idioma) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Idioma);
        나누개.setText(Conteúdo_VALOR);
        List<String> resultado = new ArrayList<>();
        int iniciar = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; iniciar = 끝, 끝 = 나누개.next())
            resultado.add(Conteúdo_VALOR.substring(iniciar, 끝));
        return resultado;
    }
}
