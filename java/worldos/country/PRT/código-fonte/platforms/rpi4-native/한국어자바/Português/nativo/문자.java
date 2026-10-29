// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Português.nativo;
/** 문자(文字), Codificação_VALOR(符號): UTF-8 바이트와 UTF-16 문자열의 CONVERTER_VALOR. normalizar_VALOR/composição_VALOR 입력기는 별개다. */
public final class 문자 {
    public static int byte_CONT_NÚM(byte[] dados) { return dados.length; }
    private 문자() {}
    public static int duração_VALOR(String texto) { return texto.length(); }
    public static boolean 같음(String câmera_frontal_VALOR, String BACK_VALOR) { return câmera_frontal_VALOR == null ? BACK_VALOR == null : câmera_frontal_VALOR.equals(BACK_VALOR); }
    public static String colar_SMS(String câmera_frontal_VALOR, String BACK_VALOR) { return câmera_frontal_VALOR.concat(BACK_VALOR); }
    public static String cortar_VALOR(String texto, int iniciar, int 끝) { return texto.substring(iniciar, 끝); }
    public static int analisar_inteiro(String texto) { try { return Integer.parseInt(texto); } catch (NumberFormatException erro) { throw new número_formato_falha("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String gravar_inteiro_VALOR(int número) { return Integer.toString(número); }
    public static int ponto_de_código_CONT_NÚM(String texto) {
        int número = 0;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < texto.length(); Loop_ÍNDICE++, número++) {
            int ponto_de_código = texto.charAt(Loop_ÍNDICE);
            if (ponto_de_código >= 0xd800 && ponto_de_código <= 0xdbff && Loop_ÍNDICE + 1 < texto.length() && texto.charAt(Loop_ÍNDICE + 1) >= 0xdc00 && texto.charAt(Loop_ÍNDICE + 1) <= 0xdfff) Loop_ÍNDICE++;
        }
        return número;
    }
    public static byte[] codificar(String texto) {
        byte[] 임시 = new byte[texto.length() * 3]; int 쓴수 = 0;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < texto.length(); Loop_ÍNDICE++) {
            int ponto_de_código = texto.charAt(Loop_ÍNDICE);
            if (ponto_de_código >= 0xd800 && ponto_de_código <= 0xdbff && Loop_ÍNDICE + 1 < texto.length() && texto.charAt(Loop_ÍNDICE + 1) >= 0xdc00 && texto.charAt(Loop_ÍNDICE + 1) <= 0xdfff) ponto_de_código = 0x10000 + ((ponto_de_código - 0xd800) << 10) + texto.charAt(++Loop_ÍNDICE) - 0xdc00;
            else if (ponto_de_código >= 0xd800 && ponto_de_código <= 0xdfff) ponto_de_código = '?';
            if (ponto_de_código < 128) 임시[쓴수++] = (byte)ponto_de_código;
            else if (ponto_de_código < 2048) { 임시[쓴수++] = (byte)(192 | ponto_de_código >> 6); 임시[쓴수++] = (byte)(128 | ponto_de_código & 63); }
            else if (ponto_de_código < 65536) { 임시[쓴수++] = (byte)(224 | ponto_de_código >> 12); 임시[쓴수++] = (byte)(128 | ponto_de_código >> 6 & 63); 임시[쓴수++] = (byte)(128 | ponto_de_código & 63); }
            else { 임시[쓴수++] = (byte)(240 | ponto_de_código >> 18); 임시[쓴수++] = (byte)(128 | ponto_de_código >> 12 & 63); 임시[쓴수++] = (byte)(128 | ponto_de_código >> 6 & 63); 임시[쓴수++] = (byte)(128 | ponto_de_código & 63); }
        }
        byte[] resultado = new byte[쓴수]; System.arraycopy(임시, 0, resultado, 0, 쓴수); return resultado;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String descriptografar_dados(byte[] byte_VALOR) {
        StringBuilder resultado = new StringBuilder();
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < byte_VALOR.length;) {
            int ponto_de_código = byte_VALOR[Loop_ÍNDICE++] & 255, número = ponto_de_código < 128 ? 0 : ponto_de_código >= 194 && ponto_de_código < 224 ? 1 : ponto_de_código >= 224 && ponto_de_código < 240 ? 2 : ponto_de_código >= 240 && ponto_de_código <= 244 ? 3 : -1;
            if (número < 0 || byte_VALOR.length - Loop_ÍNDICE < número) throw new inválido_argumento_exceção("잘못된 UTF-8");
            int 최소 = número == 1 ? 128 : número == 2 ? 2048 : número == 3 ? 65536 : 0;
            if (número > 0) ponto_de_código &= (1 << (6 - número)) - 1;
            for (int interna_cargo = 0; interna_cargo < número; interna_cargo++) { int BACK_VALOR = byte_VALOR[Loop_ÍNDICE++] & 255; if ((BACK_VALOR & 192) != 128) throw new inválido_argumento_exceção("잘못된 UTF-8"); ponto_de_código = ponto_de_código << 6 | BACK_VALOR & 63; }
            if (ponto_de_código < 최소 || ponto_de_código > 0x10ffff || ponto_de_código >= 0xd800 && ponto_de_código <= 0xdfff) throw new inválido_argumento_exceção("잘못된 UTF-8");
            if (ponto_de_código < 65536) resultado.append((char)ponto_de_código);
            else { ponto_de_código -= 65536; resultado.append((char)(0xd800 | ponto_de_código >> 10)); resultado.append((char)(0xdc00 | ponto_de_código & 1023)); }
        }
        return resultado.toString();
    }
}
