// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Malti.자체;
/** 문자(文字), kodifikar_VALUE(符號): UTF-8 바이트와 UTF-16 문자열의 CONVERT_VALUE. nnormalizza_VALUE/조합 입력기는 별개다. */
public final class 문자 {
    public static int byte_COUNT(byte[] data) { return data.length; }
    private 문자() {}
    public static int tul_VALUE(String SMS) { return SMS.length(); }
    public static boolean 같음(String 앞, String Lura_VALUE) { return 앞 == null ? Lura_VALUE == null : 앞.equals(Lura_VALUE); }
    public static String ppejstja_SMS(String 앞, String Lura_VALUE) { return 앞.concat(Lura_VALUE); }
    public static String aqta_VALUE(String SMS, int serje, int 끝) { return SMS.substring(serje, 끝); }
    public static int analizza_numru_sħiħ(String SMS) { try { return Integer.parseInt(SMS); } catch (NumberFormatException żball) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String kiteb_numru_sħiħ_VALUE(int 수) { return Integer.toString(수); }
    public static int kodiċi_tal_karattru_COUNT(String SMS) {
        int 수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < SMS.length(); Loop_INDEX++, 수++) {
            int kodiċi_tal_karattru = SMS.charAt(Loop_INDEX);
            if (kodiċi_tal_karattru >= 0xd800 && kodiċi_tal_karattru <= 0xdbff && Loop_INDEX + 1 < SMS.length() && SMS.charAt(Loop_INDEX + 1) >= 0xdc00 && SMS.charAt(Loop_INDEX + 1) <= 0xdfff) Loop_INDEX++;
        }
        return 수;
    }
    public static byte[] 부호화(String SMS) {
        byte[] 임시 = new byte[SMS.length() * 3]; int 쓴수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < SMS.length(); Loop_INDEX++) {
            int kodiċi_tal_karattru = SMS.charAt(Loop_INDEX);
            if (kodiċi_tal_karattru >= 0xd800 && kodiċi_tal_karattru <= 0xdbff && Loop_INDEX + 1 < SMS.length() && SMS.charAt(Loop_INDEX + 1) >= 0xdc00 && SMS.charAt(Loop_INDEX + 1) <= 0xdfff) kodiċi_tal_karattru = 0x10000 + ((kodiċi_tal_karattru - 0xd800) << 10) + SMS.charAt(++Loop_INDEX) - 0xdc00;
            else if (kodiċi_tal_karattru >= 0xd800 && kodiċi_tal_karattru <= 0xdfff) kodiċi_tal_karattru = '?';
            if (kodiċi_tal_karattru < 128) 임시[쓴수++] = (byte)kodiċi_tal_karattru;
            else if (kodiċi_tal_karattru < 2048) { 임시[쓴수++] = (byte)(192 | kodiċi_tal_karattru >> 6); 임시[쓴수++] = (byte)(128 | kodiċi_tal_karattru & 63); }
            else if (kodiċi_tal_karattru < 65536) { 임시[쓴수++] = (byte)(224 | kodiċi_tal_karattru >> 12); 임시[쓴수++] = (byte)(128 | kodiċi_tal_karattru >> 6 & 63); 임시[쓴수++] = (byte)(128 | kodiċi_tal_karattru & 63); }
            else { 임시[쓴수++] = (byte)(240 | kodiċi_tal_karattru >> 18); 임시[쓴수++] = (byte)(128 | kodiċi_tal_karattru >> 12 & 63); 임시[쓴수++] = (byte)(128 | kodiċi_tal_karattru >> 6 & 63); 임시[쓴수++] = (byte)(128 | kodiċi_tal_karattru & 63); }
        }
        byte[] miżura = new byte[쓴수]; System.arraycopy(임시, 0, miżura, 0, 쓴수); return miżura;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String ddeċifra_data(byte[] byte_VALUE) {
        StringBuilder miżura = new StringBuilder();
        for (int Loop_INDEX = 0; Loop_INDEX < byte_VALUE.length;) {
            int kodiċi_tal_karattru = byte_VALUE[Loop_INDEX++] & 255, 수 = kodiċi_tal_karattru < 128 ? 0 : kodiċi_tal_karattru >= 194 && kodiċi_tal_karattru < 224 ? 1 : kodiċi_tal_karattru >= 224 && kodiċi_tal_karattru < 240 ? 2 : kodiċi_tal_karattru >= 240 && kodiċi_tal_karattru <= 244 ? 3 : -1;
            if (수 < 0 || byte_VALUE.length - Loop_INDEX < 수) throw new 잘못된인수예외("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) kodiċi_tal_karattru &= (1 << (6 - 수)) - 1;
            for (int inner_join_pożizzjoni = 0; inner_join_pożizzjoni < 수; inner_join_pożizzjoni++) { int Lura_VALUE = byte_VALUE[Loop_INDEX++] & 255; if ((Lura_VALUE & 192) != 128) throw new 잘못된인수예외("잘못된 UTF-8"); kodiċi_tal_karattru = kodiċi_tal_karattru << 6 | Lura_VALUE & 63; }
            if (kodiċi_tal_karattru < 최소 || kodiċi_tal_karattru > 0x10ffff || kodiċi_tal_karattru >= 0xd800 && kodiċi_tal_karattru <= 0xdfff) throw new 잘못된인수예외("잘못된 UTF-8");
            if (kodiċi_tal_karattru < 65536) miżura.append((char)kodiċi_tal_karattru);
            else { kodiċi_tal_karattru -= 65536; miżura.append((char)(0xd800 | kodiċi_tal_karattru >> 10)); miżura.append((char)(0xdc00 | kodiċi_tal_karattru & 1023)); }
        }
        return miżura.toString();
    }
}
