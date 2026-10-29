// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 문자(文字), usimbaji_thamani(符號): UTF-8 바이트와 UTF-16 문자열의 변환. kawaidisha_thamani/조합 입력기는 별개다. */
public final class 문자 {
    public static int 바이트수(byte[] data) { return data.length; }
    private 문자() {}
    public static int urefu_thamani(String SMS) { return SMS.length(); }
    public static boolean 같음(String mbele_thamani, String Nyuma_thamani) { return mbele_thamani == null ? Nyuma_thamani == null : mbele_thamani.equals(Nyuma_thamani); }
    public static String bandika_SMS(String mbele_thamani, String Nyuma_thamani) { return mbele_thamani.concat(Nyuma_thamani); }
    public static String kata_thamani(String SMS, int endesha, int 끝) { return SMS.substring(endesha, 끝); }
    public static int changanua_namba_kamili(String SMS) { try { return Integer.parseInt(SMS); } catch (NumberFormatException kosa) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String andika_namba_kamili_thamani(int 수) { return Integer.toString(수); }
    public static int 코드포인트수(String SMS) {
        int 수 = 0;
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < SMS.length(); kitanzi_kielezo++, 수++) {
            int msimbo_wa_kibambo = SMS.charAt(kitanzi_kielezo);
            if (msimbo_wa_kibambo >= 0xd800 && msimbo_wa_kibambo <= 0xdbff && kitanzi_kielezo + 1 < SMS.length() && SMS.charAt(kitanzi_kielezo + 1) >= 0xdc00 && SMS.charAt(kitanzi_kielezo + 1) <= 0xdfff) kitanzi_kielezo++;
        }
        return 수;
    }
    public static byte[] 부호화(String SMS) {
        byte[] 임시 = new byte[SMS.length() * 3]; int 쓴수 = 0;
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < SMS.length(); kitanzi_kielezo++) {
            int msimbo_wa_kibambo = SMS.charAt(kitanzi_kielezo);
            if (msimbo_wa_kibambo >= 0xd800 && msimbo_wa_kibambo <= 0xdbff && kitanzi_kielezo + 1 < SMS.length() && SMS.charAt(kitanzi_kielezo + 1) >= 0xdc00 && SMS.charAt(kitanzi_kielezo + 1) <= 0xdfff) msimbo_wa_kibambo = 0x10000 + ((msimbo_wa_kibambo - 0xd800) << 10) + SMS.charAt(++kitanzi_kielezo) - 0xdc00;
            else if (msimbo_wa_kibambo >= 0xd800 && msimbo_wa_kibambo <= 0xdfff) msimbo_wa_kibambo = '?';
            if (msimbo_wa_kibambo < 128) 임시[쓴수++] = (byte)msimbo_wa_kibambo;
            else if (msimbo_wa_kibambo < 2048) { 임시[쓴수++] = (byte)(192 | msimbo_wa_kibambo >> 6); 임시[쓴수++] = (byte)(128 | msimbo_wa_kibambo & 63); }
            else if (msimbo_wa_kibambo < 65536) { 임시[쓴수++] = (byte)(224 | msimbo_wa_kibambo >> 12); 임시[쓴수++] = (byte)(128 | msimbo_wa_kibambo >> 6 & 63); 임시[쓴수++] = (byte)(128 | msimbo_wa_kibambo & 63); }
            else { 임시[쓴수++] = (byte)(240 | msimbo_wa_kibambo >> 18); 임시[쓴수++] = (byte)(128 | msimbo_wa_kibambo >> 12 & 63); 임시[쓴수++] = (byte)(128 | msimbo_wa_kibambo >> 6 & 63); 임시[쓴수++] = (byte)(128 | msimbo_wa_kibambo & 63); }
        }
        byte[] 결과 = new byte[쓴수]; System.arraycopy(임시, 0, 결과, 0, 쓴수); return 결과;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String simbua_fiche_data(byte[] baiti_thamani) {
        StringBuilder 결과 = new StringBuilder();
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < baiti_thamani.length;) {
            int msimbo_wa_kibambo = baiti_thamani[kitanzi_kielezo++] & 255, 수 = msimbo_wa_kibambo < 128 ? 0 : msimbo_wa_kibambo >= 194 && msimbo_wa_kibambo < 224 ? 1 : msimbo_wa_kibambo >= 224 && msimbo_wa_kibambo < 240 ? 2 : msimbo_wa_kibambo >= 240 && msimbo_wa_kibambo <= 244 ? 3 : -1;
            if (수 < 0 || baiti_thamani.length - kitanzi_kielezo < 수) throw new batili_hoja_vighairi("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) msimbo_wa_kibambo &= (1 << (6 - 수)) - 1;
            for (int 안쪽자리 = 0; 안쪽자리 < 수; 안쪽자리++) { int Nyuma_thamani = baiti_thamani[kitanzi_kielezo++] & 255; if ((Nyuma_thamani & 192) != 128) throw new batili_hoja_vighairi("잘못된 UTF-8"); msimbo_wa_kibambo = msimbo_wa_kibambo << 6 | Nyuma_thamani & 63; }
            if (msimbo_wa_kibambo < 최소 || msimbo_wa_kibambo > 0x10ffff || msimbo_wa_kibambo >= 0xd800 && msimbo_wa_kibambo <= 0xdfff) throw new batili_hoja_vighairi("잘못된 UTF-8");
            if (msimbo_wa_kibambo < 65536) 결과.append((char)msimbo_wa_kibambo);
            else { msimbo_wa_kibambo -= 65536; 결과.append((char)(0xd800 | msimbo_wa_kibambo >> 10)); 결과.append((char)(0xdc00 | msimbo_wa_kibambo & 1023)); }
        }
        return 결과.toString();
    }
}
