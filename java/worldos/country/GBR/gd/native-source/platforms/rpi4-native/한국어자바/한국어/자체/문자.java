// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 문자(文字), còdachadh_VALUE(符號): UTF-8 바이트와 UTF-16 문자열의 CONVERT_VALUE. àbhaistich_VALUE/조합 입력기는 별개다. */
public final class 문자 {
    public static int baidht_COUNT(byte[] dàta) { return dàta.length; }
    private 문자() {}
    public static int faid_VALUE(String SMS) { return SMS.length(); }
    public static boolean 같음(String 앞, String Air_ais_VALUE) { return 앞 == null ? Air_ais_VALUE == null : 앞.equals(Air_ais_VALUE); }
    public static String cuir_ann_SMS(String 앞, String Air_ais_VALUE) { return 앞.concat(Air_ais_VALUE); }
    public static String gearr_VALUE(String SMS, int ruith, int 끝) { return SMS.substring(ruith, 끝); }
    public static int 정수읽기(String SMS) { try { return Integer.parseInt(SMS); } catch (NumberFormatException Mearachd) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String sgrìobh_àireamh_shlàn_VALUE(int 수) { return Integer.toString(수); }
    public static int còd_a_charactair_COUNT(String SMS) {
        int 수 = 0;
        for (int lùb_INDEX = 0; lùb_INDEX < SMS.length(); lùb_INDEX++, 수++) {
            int còd_a_charactair = SMS.charAt(lùb_INDEX);
            if (còd_a_charactair >= 0xd800 && còd_a_charactair <= 0xdbff && lùb_INDEX + 1 < SMS.length() && SMS.charAt(lùb_INDEX + 1) >= 0xdc00 && SMS.charAt(lùb_INDEX + 1) <= 0xdfff) lùb_INDEX++;
        }
        return 수;
    }
    public static byte[] 부호화(String SMS) {
        byte[] 임시 = new byte[SMS.length() * 3]; int 쓴수 = 0;
        for (int lùb_INDEX = 0; lùb_INDEX < SMS.length(); lùb_INDEX++) {
            int còd_a_charactair = SMS.charAt(lùb_INDEX);
            if (còd_a_charactair >= 0xd800 && còd_a_charactair <= 0xdbff && lùb_INDEX + 1 < SMS.length() && SMS.charAt(lùb_INDEX + 1) >= 0xdc00 && SMS.charAt(lùb_INDEX + 1) <= 0xdfff) còd_a_charactair = 0x10000 + ((còd_a_charactair - 0xd800) << 10) + SMS.charAt(++lùb_INDEX) - 0xdc00;
            else if (còd_a_charactair >= 0xd800 && còd_a_charactair <= 0xdfff) còd_a_charactair = '?';
            if (còd_a_charactair < 128) 임시[쓴수++] = (byte)còd_a_charactair;
            else if (còd_a_charactair < 2048) { 임시[쓴수++] = (byte)(192 | còd_a_charactair >> 6); 임시[쓴수++] = (byte)(128 | còd_a_charactair & 63); }
            else if (còd_a_charactair < 65536) { 임시[쓴수++] = (byte)(224 | còd_a_charactair >> 12); 임시[쓴수++] = (byte)(128 | còd_a_charactair >> 6 & 63); 임시[쓴수++] = (byte)(128 | còd_a_charactair & 63); }
            else { 임시[쓴수++] = (byte)(240 | còd_a_charactair >> 18); 임시[쓴수++] = (byte)(128 | còd_a_charactair >> 12 & 63); 임시[쓴수++] = (byte)(128 | còd_a_charactair >> 6 & 63); 임시[쓴수++] = (byte)(128 | còd_a_charactair & 63); }
        }
        byte[] tomhas = new byte[쓴수]; System.arraycopy(임시, 0, tomhas, 0, 쓴수); return tomhas;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String dì_chrioptaich_dàta(byte[] baidht_VALUE) {
        StringBuilder tomhas = new StringBuilder();
        for (int lùb_INDEX = 0; lùb_INDEX < baidht_VALUE.length;) {
            int còd_a_charactair = baidht_VALUE[lùb_INDEX++] & 255, 수 = còd_a_charactair < 128 ? 0 : còd_a_charactair >= 194 && còd_a_charactair < 224 ? 1 : còd_a_charactair >= 224 && còd_a_charactair < 240 ? 2 : còd_a_charactair >= 240 && còd_a_charactair <= 244 ? 3 : -1;
            if (수 < 0 || baidht_VALUE.length - lùb_INDEX < 수) throw new 잘못된인수예외("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) còd_a_charactair &= (1 << (6 - 수)) - 1;
            for (int Inner_Join_suidhich = 0; Inner_Join_suidhich < 수; Inner_Join_suidhich++) { int Air_ais_VALUE = baidht_VALUE[lùb_INDEX++] & 255; if ((Air_ais_VALUE & 192) != 128) throw new 잘못된인수예외("잘못된 UTF-8"); còd_a_charactair = còd_a_charactair << 6 | Air_ais_VALUE & 63; }
            if (còd_a_charactair < 최소 || còd_a_charactair > 0x10ffff || còd_a_charactair >= 0xd800 && còd_a_charactair <= 0xdfff) throw new 잘못된인수예외("잘못된 UTF-8");
            if (còd_a_charactair < 65536) tomhas.append((char)còd_a_charactair);
            else { còd_a_charactair -= 65536; tomhas.append((char)(0xd800 | còd_a_charactair >> 10)); tomhas.append((char)(0xdc00 | còd_a_charactair & 1023)); }
        }
        return tomhas.toString();
    }
}
