// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Română.propriu;
/** 문자(文字), codificare_VALUE(符號): UTF-8 바이트와 UTF-16 문자열의 CONVERT_VALUE. normaliza_VALUE/조합 입력기는 별개다. */
public final class 문자 {
    public static int byte_COUNT(byte[] date) { return date.length; }
    private 문자() {}
    public static int lungime_VALUE(String SMS) { return SMS.length(); }
    public static boolean 같음(String frontală_VALUE, String ÎNAPOI_VALUE) { return frontală_VALUE == null ? ÎNAPOI_VALUE == null : frontală_VALUE.equals(ÎNAPOI_VALUE); }
    public static String lipi_SMS(String frontală_VALUE, String ÎNAPOI_VALUE) { return frontală_VALUE.concat(ÎNAPOI_VALUE); }
    public static String decupa_VALUE(String SMS, int Pornește, int 끝) { return SMS.substring(Pornește, 끝); }
    public static int analiza_întreg(String SMS) { try { return Integer.parseInt(SMS); } catch (NumberFormatException eroare) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String scriere_întreg_VALUE(int 수) { return Integer.toString(수); }
    public static int cod_caracter_COUNT(String SMS) {
        int 수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < SMS.length(); Loop_INDEX++, 수++) {
            int cod_caracter = SMS.charAt(Loop_INDEX);
            if (cod_caracter >= 0xd800 && cod_caracter <= 0xdbff && Loop_INDEX + 1 < SMS.length() && SMS.charAt(Loop_INDEX + 1) >= 0xdc00 && SMS.charAt(Loop_INDEX + 1) <= 0xdfff) Loop_INDEX++;
        }
        return 수;
    }
    public static byte[] codifica(String SMS) {
        byte[] 임시 = new byte[SMS.length() * 3]; int 쓴수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < SMS.length(); Loop_INDEX++) {
            int cod_caracter = SMS.charAt(Loop_INDEX);
            if (cod_caracter >= 0xd800 && cod_caracter <= 0xdbff && Loop_INDEX + 1 < SMS.length() && SMS.charAt(Loop_INDEX + 1) >= 0xdc00 && SMS.charAt(Loop_INDEX + 1) <= 0xdfff) cod_caracter = 0x10000 + ((cod_caracter - 0xd800) << 10) + SMS.charAt(++Loop_INDEX) - 0xdc00;
            else if (cod_caracter >= 0xd800 && cod_caracter <= 0xdfff) cod_caracter = '?';
            if (cod_caracter < 128) 임시[쓴수++] = (byte)cod_caracter;
            else if (cod_caracter < 2048) { 임시[쓴수++] = (byte)(192 | cod_caracter >> 6); 임시[쓴수++] = (byte)(128 | cod_caracter & 63); }
            else if (cod_caracter < 65536) { 임시[쓴수++] = (byte)(224 | cod_caracter >> 12); 임시[쓴수++] = (byte)(128 | cod_caracter >> 6 & 63); 임시[쓴수++] = (byte)(128 | cod_caracter & 63); }
            else { 임시[쓴수++] = (byte)(240 | cod_caracter >> 18); 임시[쓴수++] = (byte)(128 | cod_caracter >> 12 & 63); 임시[쓴수++] = (byte)(128 | cod_caracter >> 6 & 63); 임시[쓴수++] = (byte)(128 | cod_caracter & 63); }
        }
        byte[] KR = new byte[쓴수]; System.arraycopy(임시, 0, KR, 0, 쓴수); return KR;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String decripta_date(byte[] byte_VALUE) {
        StringBuilder KR = new StringBuilder();
        for (int Loop_INDEX = 0; Loop_INDEX < byte_VALUE.length;) {
            int cod_caracter = byte_VALUE[Loop_INDEX++] & 255, 수 = cod_caracter < 128 ? 0 : cod_caracter >= 194 && cod_caracter < 224 ? 1 : cod_caracter >= 224 && cod_caracter < 240 ? 2 : cod_caracter >= 240 && cod_caracter <= 244 ? 3 : -1;
            if (수 < 0 || byte_VALUE.length - Loop_INDEX < 수) throw new nul_argument_excepție("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) cod_caracter &= (1 << (6 - 수)) - 1;
            for (int internă_poziție = 0; internă_poziție < 수; internă_poziție++) { int ÎNAPOI_VALUE = byte_VALUE[Loop_INDEX++] & 255; if ((ÎNAPOI_VALUE & 192) != 128) throw new nul_argument_excepție("잘못된 UTF-8"); cod_caracter = cod_caracter << 6 | ÎNAPOI_VALUE & 63; }
            if (cod_caracter < 최소 || cod_caracter > 0x10ffff || cod_caracter >= 0xd800 && cod_caracter <= 0xdfff) throw new nul_argument_excepție("잘못된 UTF-8");
            if (cod_caracter < 65536) KR.append((char)cod_caracter);
            else { cod_caracter -= 65536; KR.append((char)(0xd800 | cod_caracter >> 10)); KR.append((char)(0xdc00 | cod_caracter & 1023)); }
        }
        return KR.toString();
    }
}
