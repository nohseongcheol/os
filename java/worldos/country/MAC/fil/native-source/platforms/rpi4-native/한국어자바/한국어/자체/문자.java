// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 문자(文字), pag_encode_VALUE(符號): UTF-8 바이트와 UTF-16 문자열의 CONVERT_VALUE. normalisahin_VALUE/조합 입력기는 별개다. */
public final class 문자 {
    public static int byte_COUNT(byte[] data) { return data.length; }
    private 문자() {}
    public static int haba_VALUE(String SMS) { return SMS.length(); }
    public static boolean 같음(String nasa_harap_VALUE, String Bumalik_VALUE) { return nasa_harap_VALUE == null ? Bumalik_VALUE == null : nasa_harap_VALUE.equals(Bumalik_VALUE); }
    public static String I_paste_SMS(String nasa_harap_VALUE, String Bumalik_VALUE) { return nasa_harap_VALUE.concat(Bumalik_VALUE); }
    public static String I_cut_VALUE(String SMS, int run, int 끝) { return SMS.substring(run, 끝); }
    public static int mag_parse_integer_buong_numero(String SMS) { try { return Integer.parseInt(SMS); } catch (NumberFormatException error) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String sumulat_integer_buong_numero_VALUE(int 수) { return Integer.toString(수); }
    public static int character_code_COUNT(String SMS) {
        int 수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < SMS.length(); Loop_INDEX++, 수++) {
            int character_code = SMS.charAt(Loop_INDEX);
            if (character_code >= 0xd800 && character_code <= 0xdbff && Loop_INDEX + 1 < SMS.length() && SMS.charAt(Loop_INDEX + 1) >= 0xdc00 && SMS.charAt(Loop_INDEX + 1) <= 0xdfff) Loop_INDEX++;
        }
        return 수;
    }
    public static byte[] 부호화(String SMS) {
        byte[] 임시 = new byte[SMS.length() * 3]; int 쓴수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < SMS.length(); Loop_INDEX++) {
            int character_code = SMS.charAt(Loop_INDEX);
            if (character_code >= 0xd800 && character_code <= 0xdbff && Loop_INDEX + 1 < SMS.length() && SMS.charAt(Loop_INDEX + 1) >= 0xdc00 && SMS.charAt(Loop_INDEX + 1) <= 0xdfff) character_code = 0x10000 + ((character_code - 0xd800) << 10) + SMS.charAt(++Loop_INDEX) - 0xdc00;
            else if (character_code >= 0xd800 && character_code <= 0xdfff) character_code = '?';
            if (character_code < 128) 임시[쓴수++] = (byte)character_code;
            else if (character_code < 2048) { 임시[쓴수++] = (byte)(192 | character_code >> 6); 임시[쓴수++] = (byte)(128 | character_code & 63); }
            else if (character_code < 65536) { 임시[쓴수++] = (byte)(224 | character_code >> 12); 임시[쓴수++] = (byte)(128 | character_code >> 6 & 63); 임시[쓴수++] = (byte)(128 | character_code & 63); }
            else { 임시[쓴수++] = (byte)(240 | character_code >> 18); 임시[쓴수++] = (byte)(128 | character_code >> 12 & 63); 임시[쓴수++] = (byte)(128 | character_code >> 6 & 63); 임시[쓴수++] = (byte)(128 | character_code & 63); }
        }
        byte[] sukat = new byte[쓴수]; System.arraycopy(임시, 0, sukat, 0, 쓴수); return sukat;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String i_decrypt_data(byte[] byte_VALUE) {
        StringBuilder sukat = new StringBuilder();
        for (int Loop_INDEX = 0; Loop_INDEX < byte_VALUE.length;) {
            int character_code = byte_VALUE[Loop_INDEX++] & 255, 수 = character_code < 128 ? 0 : character_code >= 194 && character_code < 224 ? 1 : character_code >= 224 && character_code < 240 ? 2 : character_code >= 240 && character_code <= 244 ? 3 : -1;
            if (수 < 0 || byte_VALUE.length - Loop_INDEX < 수) throw new hindi_tama_argumento_pagbubukod("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) character_code &= (1 << (6 - 수)) - 1;
            for (int inner_join_posisyon = 0; inner_join_posisyon < 수; inner_join_posisyon++) { int Bumalik_VALUE = byte_VALUE[Loop_INDEX++] & 255; if ((Bumalik_VALUE & 192) != 128) throw new hindi_tama_argumento_pagbubukod("잘못된 UTF-8"); character_code = character_code << 6 | Bumalik_VALUE & 63; }
            if (character_code < 최소 || character_code > 0x10ffff || character_code >= 0xd800 && character_code <= 0xdfff) throw new hindi_tama_argumento_pagbubukod("잘못된 UTF-8");
            if (character_code < 65536) sukat.append((char)character_code);
            else { character_code -= 65536; sukat.append((char)(0xd800 | character_code >> 10)); sukat.append((char)(0xdc00 | character_code & 1023)); }
        }
        return sukat.toString();
    }
}
