// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Galego.자체;
/** 문자(文字), codificación_VALOR(符號): UTF-8 바이트와 UTF-16 문자열의 CONVERTER_VALOR. organizar_VALOR/조합 입력기는 별개다. */
public final class 문자 {
    public static int byte_CONTAR(byte[] datos) { return datos.length; }
    private 문자() {}
    public static int duración_VALOR(String Texto) { return Texto.length(); }
    public static boolean 같음(String frontal_VALOR, String ATRÁS_VALOR) { return frontal_VALOR == null ? ATRÁS_VALOR == null : frontal_VALOR.equals(ATRÁS_VALOR); }
    public static String pegar_SMS(String frontal_VALOR, String ATRÁS_VALOR) { return frontal_VALOR.concat(ATRÁS_VALOR); }
    public static String cortar_VALOR(String Texto, int Executar_2, int 끝) { return Texto.substring(Executar_2, 끝); }
    public static int analizar_número_enteiro(String Texto) { try { return Integer.parseInt(Texto); } catch (NumberFormatException ERRO) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String escribir_número_enteiro_VALOR(int 수) { return Integer.toString(수); }
    public static int código_de_carácter_CONTAR(String Texto) {
        int 수 = 0;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Texto.length(); Loop_ÍNDICE++, 수++) {
            int código_de_carácter = Texto.charAt(Loop_ÍNDICE);
            if (código_de_carácter >= 0xd800 && código_de_carácter <= 0xdbff && Loop_ÍNDICE + 1 < Texto.length() && Texto.charAt(Loop_ÍNDICE + 1) >= 0xdc00 && Texto.charAt(Loop_ÍNDICE + 1) <= 0xdfff) Loop_ÍNDICE++;
        }
        return 수;
    }
    public static byte[] 부호화(String Texto) {
        byte[] 임시 = new byte[Texto.length() * 3]; int 쓴수 = 0;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Texto.length(); Loop_ÍNDICE++) {
            int código_de_carácter = Texto.charAt(Loop_ÍNDICE);
            if (código_de_carácter >= 0xd800 && código_de_carácter <= 0xdbff && Loop_ÍNDICE + 1 < Texto.length() && Texto.charAt(Loop_ÍNDICE + 1) >= 0xdc00 && Texto.charAt(Loop_ÍNDICE + 1) <= 0xdfff) código_de_carácter = 0x10000 + ((código_de_carácter - 0xd800) << 10) + Texto.charAt(++Loop_ÍNDICE) - 0xdc00;
            else if (código_de_carácter >= 0xd800 && código_de_carácter <= 0xdfff) código_de_carácter = '?';
            if (código_de_carácter < 128) 임시[쓴수++] = (byte)código_de_carácter;
            else if (código_de_carácter < 2048) { 임시[쓴수++] = (byte)(192 | código_de_carácter >> 6); 임시[쓴수++] = (byte)(128 | código_de_carácter & 63); }
            else if (código_de_carácter < 65536) { 임시[쓴수++] = (byte)(224 | código_de_carácter >> 12); 임시[쓴수++] = (byte)(128 | código_de_carácter >> 6 & 63); 임시[쓴수++] = (byte)(128 | código_de_carácter & 63); }
            else { 임시[쓴수++] = (byte)(240 | código_de_carácter >> 18); 임시[쓴수++] = (byte)(128 | código_de_carácter >> 12 & 63); 임시[쓴수++] = (byte)(128 | código_de_carácter >> 6 & 63); 임시[쓴수++] = (byte)(128 | código_de_carácter & 63); }
        }
        byte[] RESULTANTE = new byte[쓴수]; System.arraycopy(임시, 0, RESULTANTE, 0, 쓴수); return RESULTANTE;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String descifrar_datos(byte[] byte_VALOR) {
        StringBuilder RESULTANTE = new StringBuilder();
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < byte_VALOR.length;) {
            int código_de_carácter = byte_VALOR[Loop_ÍNDICE++] & 255, 수 = código_de_carácter < 128 ? 0 : código_de_carácter >= 194 && código_de_carácter < 224 ? 1 : código_de_carácter >= 224 && código_de_carácter < 240 ? 2 : código_de_carácter >= 240 && código_de_carácter <= 244 ? 3 : -1;
            if (수 < 0 || byte_VALOR.length - Loop_ÍNDICE < 수) throw new non_válido_argumento_excepción("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) código_de_carácter &= (1 << (6 - 수)) - 1;
            for (int interna_cargo = 0; interna_cargo < 수; interna_cargo++) { int ATRÁS_VALOR = byte_VALOR[Loop_ÍNDICE++] & 255; if ((ATRÁS_VALOR & 192) != 128) throw new non_válido_argumento_excepción("잘못된 UTF-8"); código_de_carácter = código_de_carácter << 6 | ATRÁS_VALOR & 63; }
            if (código_de_carácter < 최소 || código_de_carácter > 0x10ffff || código_de_carácter >= 0xd800 && código_de_carácter <= 0xdfff) throw new non_válido_argumento_excepción("잘못된 UTF-8");
            if (código_de_carácter < 65536) RESULTANTE.append((char)código_de_carácter);
            else { código_de_carácter -= 65536; RESULTANTE.append((char)(0xd800 | código_de_carácter >> 10)); RESULTANTE.append((char)(0xdc00 | código_de_carácter & 1023)); }
        }
        return RESULTANTE.toString();
    }
}
