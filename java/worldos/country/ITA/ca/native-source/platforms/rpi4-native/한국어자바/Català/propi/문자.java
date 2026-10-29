// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Català.propi;
/** 문자(文字), codificació_VALOR(符號): UTF-8 바이트와 UTF-16 문자열의 CONVERT_VALOR. normalitzar_VALOR/조합 입력기는 별개다. */
public final class 문자 {
    public static int byte_COMPT(byte[] dades) { return dades.length; }
    private 문자() {}
    public static int durada_VALOR(String SMS) { return SMS.length(); }
    public static boolean 같음(String frontal_VALOR, String ENRERE_VALOR) { return frontal_VALOR == null ? ENRERE_VALOR == null : frontal_VALOR.equals(ENRERE_VALOR); }
    public static String enganxar_SMS(String frontal_VALOR, String ENRERE_VALOR) { return frontal_VALOR.concat(ENRERE_VALOR); }
    public static String tallar_VALOR(String SMS, int Executa_2, int 끝) { return SMS.substring(Executa_2, 끝); }
    public static int 정수읽기(String SMS) { try { return Integer.parseInt(SMS); } catch (NumberFormatException s_ha_produït_un_error) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String 정수쓰기(int 수) { return Integer.toString(수); }
    public static int codi_de_caràcter_COMPT(String SMS) {
        int 수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < SMS.length(); Loop_INDEX++, 수++) {
            int codi_de_caràcter = SMS.charAt(Loop_INDEX);
            if (codi_de_caràcter >= 0xd800 && codi_de_caràcter <= 0xdbff && Loop_INDEX + 1 < SMS.length() && SMS.charAt(Loop_INDEX + 1) >= 0xdc00 && SMS.charAt(Loop_INDEX + 1) <= 0xdfff) Loop_INDEX++;
        }
        return 수;
    }
    public static byte[] 부호화(String SMS) {
        byte[] 임시 = new byte[SMS.length() * 3]; int 쓴수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < SMS.length(); Loop_INDEX++) {
            int codi_de_caràcter = SMS.charAt(Loop_INDEX);
            if (codi_de_caràcter >= 0xd800 && codi_de_caràcter <= 0xdbff && Loop_INDEX + 1 < SMS.length() && SMS.charAt(Loop_INDEX + 1) >= 0xdc00 && SMS.charAt(Loop_INDEX + 1) <= 0xdfff) codi_de_caràcter = 0x10000 + ((codi_de_caràcter - 0xd800) << 10) + SMS.charAt(++Loop_INDEX) - 0xdc00;
            else if (codi_de_caràcter >= 0xd800 && codi_de_caràcter <= 0xdfff) codi_de_caràcter = '?';
            if (codi_de_caràcter < 128) 임시[쓴수++] = (byte)codi_de_caràcter;
            else if (codi_de_caràcter < 2048) { 임시[쓴수++] = (byte)(192 | codi_de_caràcter >> 6); 임시[쓴수++] = (byte)(128 | codi_de_caràcter & 63); }
            else if (codi_de_caràcter < 65536) { 임시[쓴수++] = (byte)(224 | codi_de_caràcter >> 12); 임시[쓴수++] = (byte)(128 | codi_de_caràcter >> 6 & 63); 임시[쓴수++] = (byte)(128 | codi_de_caràcter & 63); }
            else { 임시[쓴수++] = (byte)(240 | codi_de_caràcter >> 18); 임시[쓴수++] = (byte)(128 | codi_de_caràcter >> 12 & 63); 임시[쓴수++] = (byte)(128 | codi_de_caràcter >> 6 & 63); 임시[쓴수++] = (byte)(128 | codi_de_caràcter & 63); }
        }
        byte[] RESULTAT = new byte[쓴수]; System.arraycopy(임시, 0, RESULTAT, 0, 쓴수); return RESULTAT;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String desencriptar_dades(byte[] byte_VALOR) {
        StringBuilder RESULTAT = new StringBuilder();
        for (int Loop_INDEX = 0; Loop_INDEX < byte_VALOR.length;) {
            int codi_de_caràcter = byte_VALOR[Loop_INDEX++] & 255, 수 = codi_de_caràcter < 128 ? 0 : codi_de_caràcter >= 194 && codi_de_caràcter < 224 ? 1 : codi_de_caràcter >= 224 && codi_de_caràcter < 240 ? 2 : codi_de_caràcter >= 240 && codi_de_caràcter <= 244 ? 3 : -1;
            if (수 < 0 || byte_VALOR.length - Loop_INDEX < 수) throw new invàlid_arg_excepció("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) codi_de_caràcter &= (1 << (6 - 수)) - 1;
            for (int interna_càrrec = 0; interna_càrrec < 수; interna_càrrec++) { int ENRERE_VALOR = byte_VALOR[Loop_INDEX++] & 255; if ((ENRERE_VALOR & 192) != 128) throw new invàlid_arg_excepció("잘못된 UTF-8"); codi_de_caràcter = codi_de_caràcter << 6 | ENRERE_VALOR & 63; }
            if (codi_de_caràcter < 최소 || codi_de_caràcter > 0x10ffff || codi_de_caràcter >= 0xd800 && codi_de_caràcter <= 0xdfff) throw new invàlid_arg_excepció("잘못된 UTF-8");
            if (codi_de_caràcter < 65536) RESULTAT.append((char)codi_de_caràcter);
            else { codi_de_caràcter -= 65536; RESULTAT.append((char)(0xd800 | codi_de_caràcter >> 10)); RESULTAT.append((char)(0xdc00 | codi_de_caràcter & 1023)); }
        }
        return RESULTAT.toString();
    }
}
