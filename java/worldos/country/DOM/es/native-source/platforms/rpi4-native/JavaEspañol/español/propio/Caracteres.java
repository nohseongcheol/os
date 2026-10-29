// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.propio;
/** Convierte entre bytes UTF-8 y cadenas UTF-16. La normalización y la entrada compuesta se tratan por separado. */
public final class Caracteres {
    public static int númeroElementosByte(byte[] Datos) { return Datos.length; }
    private Caracteres() {}
    public static int longitud(String texto) { return texto.length(); }
    public static boolean textoIgual(String valorLadoDelantero, String valorLadoPosterior) { return valorLadoDelantero == null ? valorLadoPosterior == null : valorLadoDelantero.equals(valorLadoPosterior); }
    public static String textoPegar(String valorLadoDelantero, String valorLadoPosterior) { return valorLadoDelantero.concat(valorLadoPosterior); }
    public static String valorCortar(String texto, int ponerEnMarcha, int terminación) { return texto.substring(ponerEnMarcha, terminación); }
    public static int analizarEnteroValor(String texto) { try { return Integer.parseInt(texto); } catch (NumberFormatException error) { throw new FalloFormatoNúmero("Compruebe el formato y el intervalo del número."); } }
    public static String escribirValorEnteroValor(int númeroValor) { return Integer.toString(númeroValor); }
    public static int númeroElementosPuntoCódigo(String texto) {
        int númeroValor = 0;
        for (int índiceBucle = 0; índiceBucle < texto.length(); índiceBucle++, númeroValor++) {
            int códigoCarácter = texto.charAt(índiceBucle);
            if (códigoCarácter >= 0xd800 && códigoCarácter <= 0xdbff && índiceBucle + 1 < texto.length() && texto.charAt(índiceBucle + 1) >= 0xdc00 && texto.charAt(índiceBucle + 1) <= 0xdfff) índiceBucle++;
        }
        return númeroValor;
    }
    public static byte[] codificar(String texto) {
        byte[] valorTemporal = new byte[texto.length() * 3]; int escrito = 0;
        for (int índiceBucle = 0; índiceBucle < texto.length(); índiceBucle++) {
            int códigoCarácter = texto.charAt(índiceBucle);
            if (códigoCarácter >= 0xd800 && códigoCarácter <= 0xdbff && índiceBucle + 1 < texto.length() && texto.charAt(índiceBucle + 1) >= 0xdc00 && texto.charAt(índiceBucle + 1) <= 0xdfff) códigoCarácter = 0x10000 + ((códigoCarácter - 0xd800) << 10) + texto.charAt(++índiceBucle) - 0xdc00;
            else if (códigoCarácter >= 0xd800 && códigoCarácter <= 0xdfff) códigoCarácter = '?';
            if (códigoCarácter < 128) valorTemporal[escrito++] = (byte)códigoCarácter;
            else if (códigoCarácter < 2048) { valorTemporal[escrito++] = (byte)(192 | códigoCarácter >> 6); valorTemporal[escrito++] = (byte)(128 | códigoCarácter & 63); }
            else if (códigoCarácter < 65536) { valorTemporal[escrito++] = (byte)(224 | códigoCarácter >> 12); valorTemporal[escrito++] = (byte)(128 | códigoCarácter >> 6 & 63); valorTemporal[escrito++] = (byte)(128 | códigoCarácter & 63); }
            else { valorTemporal[escrito++] = (byte)(240 | códigoCarácter >> 18); valorTemporal[escrito++] = (byte)(128 | códigoCarácter >> 12 & 63); valorTemporal[escrito++] = (byte)(128 | códigoCarácter >> 6 & 63); valorTemporal[escrito++] = (byte)(128 | códigoCarácter & 63); }
        }
        byte[] resultado = new byte[escrito]; System.arraycopy(valorTemporal, 0, resultado, 0, escrito); return resultado;
    }
    /** Rechaza UTF-8 mal formado con la excepción de argumento no válido de la API. */
    public static String descifrarDatos(byte[] valorByte) {
        StringBuilder resultado = new StringBuilder();
        for (int índiceBucle = 0; índiceBucle < valorByte.length;) {
            int códigoCarácter = valorByte[índiceBucle++] & 255, númeroValor = códigoCarácter < 128 ? 0 : códigoCarácter >= 194 && códigoCarácter < 224 ? 1 : códigoCarácter >= 224 && códigoCarácter < 240 ? 2 : códigoCarácter >= 240 && códigoCarácter <= 244 ? 3 : -1;
            if (númeroValor < 0 || valorByte.length - índiceBucle < númeroValor) throw new ExcepciónArgumentoInválido("UTF-8 no válido");
            int valorMínimo = númeroValor == 1 ? 128 : númeroValor == 2 ? 2048 : númeroValor == 3 ? 65536 : 0;
            if (númeroValor > 0) códigoCarácter &= (1 << (6 - númeroValor)) - 1;
            for (int posiciónInterior = 0; posiciónInterior < númeroValor; posiciónInterior++) { int valorLadoPosterior = valorByte[índiceBucle++] & 255; if ((valorLadoPosterior & 192) != 128) throw new ExcepciónArgumentoInválido("UTF-8 no válido"); códigoCarácter = códigoCarácter << 6 | valorLadoPosterior & 63; }
            if (códigoCarácter < valorMínimo || códigoCarácter > 0x10ffff || códigoCarácter >= 0xd800 && códigoCarácter <= 0xdfff) throw new ExcepciónArgumentoInválido("UTF-8 no válido");
            if (códigoCarácter < 65536) resultado.append((char)códigoCarácter);
            else { códigoCarácter -= 65536; resultado.append((char)(0xd800 | códigoCarácter >> 10)); resultado.append((char)(0xdc00 | códigoCarácter & 1023)); }
        }
        return resultado.toString();
    }
}
