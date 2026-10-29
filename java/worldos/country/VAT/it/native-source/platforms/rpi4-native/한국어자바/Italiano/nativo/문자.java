// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italiano.nativo;
/** 문자(文字), Codifica_VALORE(符號): UTF-8 바이트와 UTF-16 문자열의 CONVERTI_VALORE. normalizzare_VALORE/composizione_VALORE 입력기는 별개다. */
public final class 문자 {
    public static int byte_CONTA_NUMERI(byte[] dati) { return dati.length; }
    private 문자() {}
    public static int durata_VALORE(String testo) { return testo.length(); }
    public static boolean 같음(String frontale_VALORE, String BACK_VALORE) { return frontale_VALORE == null ? BACK_VALORE == null : frontale_VALORE.equals(BACK_VALORE); }
    public static String incollare_SMS(String frontale_VALORE, String BACK_VALORE) { return frontale_VALORE.concat(BACK_VALORE); }
    public static String tagliare_VALORE(String testo, int avvia, int 끝) { return testo.substring(avvia, 끝); }
    public static int analizzare_intero(String testo) { try { return Integer.parseInt(testo); } catch (NumberFormatException errore) { throw new numero_formato_errore("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String scrivere_intero_VALORE(int numero) { return Integer.toString(numero); }
    public static int punto_di_codice_CONTA_NUMERI(String testo) {
        int numero = 0;
        for (int Loop_INDICE = 0; Loop_INDICE < testo.length(); Loop_INDICE++, numero++) {
            int punto_di_codice = testo.charAt(Loop_INDICE);
            if (punto_di_codice >= 0xd800 && punto_di_codice <= 0xdbff && Loop_INDICE + 1 < testo.length() && testo.charAt(Loop_INDICE + 1) >= 0xdc00 && testo.charAt(Loop_INDICE + 1) <= 0xdfff) Loop_INDICE++;
        }
        return numero;
    }
    public static byte[] codificare(String testo) {
        byte[] 임시 = new byte[testo.length() * 3]; int 쓴수 = 0;
        for (int Loop_INDICE = 0; Loop_INDICE < testo.length(); Loop_INDICE++) {
            int punto_di_codice = testo.charAt(Loop_INDICE);
            if (punto_di_codice >= 0xd800 && punto_di_codice <= 0xdbff && Loop_INDICE + 1 < testo.length() && testo.charAt(Loop_INDICE + 1) >= 0xdc00 && testo.charAt(Loop_INDICE + 1) <= 0xdfff) punto_di_codice = 0x10000 + ((punto_di_codice - 0xd800) << 10) + testo.charAt(++Loop_INDICE) - 0xdc00;
            else if (punto_di_codice >= 0xd800 && punto_di_codice <= 0xdfff) punto_di_codice = '?';
            if (punto_di_codice < 128) 임시[쓴수++] = (byte)punto_di_codice;
            else if (punto_di_codice < 2048) { 임시[쓴수++] = (byte)(192 | punto_di_codice >> 6); 임시[쓴수++] = (byte)(128 | punto_di_codice & 63); }
            else if (punto_di_codice < 65536) { 임시[쓴수++] = (byte)(224 | punto_di_codice >> 12); 임시[쓴수++] = (byte)(128 | punto_di_codice >> 6 & 63); 임시[쓴수++] = (byte)(128 | punto_di_codice & 63); }
            else { 임시[쓴수++] = (byte)(240 | punto_di_codice >> 18); 임시[쓴수++] = (byte)(128 | punto_di_codice >> 12 & 63); 임시[쓴수++] = (byte)(128 | punto_di_codice >> 6 & 63); 임시[쓴수++] = (byte)(128 | punto_di_codice & 63); }
        }
        byte[] risultato = new byte[쓴수]; System.arraycopy(임시, 0, risultato, 0, 쓴수); return risultato;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String decifrare_dati(byte[] byte_VALORE) {
        StringBuilder risultato = new StringBuilder();
        for (int Loop_INDICE = 0; Loop_INDICE < byte_VALORE.length;) {
            int punto_di_codice = byte_VALORE[Loop_INDICE++] & 255, numero = punto_di_codice < 128 ? 0 : punto_di_codice >= 194 && punto_di_codice < 224 ? 1 : punto_di_codice >= 224 && punto_di_codice < 240 ? 2 : punto_di_codice >= 240 && punto_di_codice <= 244 ? 3 : -1;
            if (numero < 0 || byte_VALORE.length - Loop_INDICE < numero) throw new non_valida_argomento_eccezione("잘못된 UTF-8");
            int 최소 = numero == 1 ? 128 : numero == 2 ? 2048 : numero == 3 ? 65536 : 0;
            if (numero > 0) punto_di_codice &= (1 << (6 - numero)) - 1;
            for (int inner_funzione = 0; inner_funzione < numero; inner_funzione++) { int BACK_VALORE = byte_VALORE[Loop_INDICE++] & 255; if ((BACK_VALORE & 192) != 128) throw new non_valida_argomento_eccezione("잘못된 UTF-8"); punto_di_codice = punto_di_codice << 6 | BACK_VALORE & 63; }
            if (punto_di_codice < 최소 || punto_di_codice > 0x10ffff || punto_di_codice >= 0xd800 && punto_di_codice <= 0xdfff) throw new non_valida_argomento_eccezione("잘못된 UTF-8");
            if (punto_di_codice < 65536) risultato.append((char)punto_di_codice);
            else { punto_di_codice -= 65536; risultato.append((char)(0xd800 | punto_di_codice >> 10)); risultato.append((char)(0xdc00 | punto_di_codice & 1023)); }
        }
        return risultato.toString();
    }
}
