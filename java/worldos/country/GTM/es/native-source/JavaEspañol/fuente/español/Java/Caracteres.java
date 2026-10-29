// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.Java;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** Distingue el número de char UTF-16 del número de puntos de código Unicode. */
public final class Caracteres {
    private Caracteres() {}
    public static byte[] codificar(String valorContenidoValor) { return valorContenidoValor.getBytes(StandardCharsets.UTF_8); }
    public static String descifrarDatos(byte[] valorContenidoValor) { return new String(valorContenidoValor, StandardCharsets.UTF_8); }
    public static String normalizarValor(String valorContenidoValor) { return Normalizer.normalize(valorContenidoValor, Normalizer.Form.NFC); }
    public static int númeroElementosPuntoCódigo(String valorContenidoValor) { return valorContenidoValor.codePointCount(0, valorContenidoValor.length()); }
    public static List<String> palabraLéxico(String valorContenidoValor, Locale Lengua) {
        BreakIterator valorDivisor = BreakIterator.getWordInstance(Lengua);
        valorDivisor.setText(valorContenidoValor);
        List<String> resultado = new ArrayList<>();
        int ponerEnMarcha = valorDivisor.first();
        for (int terminación = valorDivisor.next(); terminación != BreakIterator.DONE; ponerEnMarcha = terminación, terminación = valorDivisor.next())
            resultado.add(valorContenidoValor.substring(ponerEnMarcha, terminación));
        return resultado;
    }
}
