// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ikinyarwanda.자체;
/** 문자(文字), gusobeka_agaciro(符號): UTF-8 바이트와 UTF-16 문자열의 변환. kuboneza_agaciro/조합 입력기는 별개다. */
public final class 문자 {
    public static int 바이트수(byte[] amakurushingiro) { return amakurushingiro.length; }
    private 문자() {}
    public static int uburebure_agaciro(String Umwandiko) { return Umwandiko.length(); }
    public static boolean 같음(String 앞, String Ikibanza_agaciro) { return 앞 == null ? Ikibanza_agaciro == null : 앞.equals(Ikibanza_agaciro); }
    public static String komeka_SMS(String 앞, String Ikibanza_agaciro) { return 앞.concat(Ikibanza_agaciro); }
    public static String gukata_agaciro(String Umwandiko, int ihuriro, int 끝) { return Umwandiko.substring(ihuriro, 끝); }
    public static int gusesengura_umubare_wuzuye(String Umwandiko) { try { return Integer.parseInt(Umwandiko); } catch (NumberFormatException IKOSA) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String kwandika_umubare_wuzuye_agaciro(int 수) { return Integer.toString(수); }
    public static int 코드포인트수(String Umwandiko) {
        int 수 = 0;
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < Umwandiko.length(); gukora_mu_matsinda_umugerekashakiro++, 수++) {
            int 문자값 = Umwandiko.charAt(gukora_mu_matsinda_umugerekashakiro);
            if (문자값 >= 0xd800 && 문자값 <= 0xdbff && gukora_mu_matsinda_umugerekashakiro + 1 < Umwandiko.length() && Umwandiko.charAt(gukora_mu_matsinda_umugerekashakiro + 1) >= 0xdc00 && Umwandiko.charAt(gukora_mu_matsinda_umugerekashakiro + 1) <= 0xdfff) gukora_mu_matsinda_umugerekashakiro++;
        }
        return 수;
    }
    public static byte[] 부호화(String Umwandiko) {
        byte[] 임시 = new byte[Umwandiko.length() * 3]; int 쓴수 = 0;
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < Umwandiko.length(); gukora_mu_matsinda_umugerekashakiro++) {
            int 문자값 = Umwandiko.charAt(gukora_mu_matsinda_umugerekashakiro);
            if (문자값 >= 0xd800 && 문자값 <= 0xdbff && gukora_mu_matsinda_umugerekashakiro + 1 < Umwandiko.length() && Umwandiko.charAt(gukora_mu_matsinda_umugerekashakiro + 1) >= 0xdc00 && Umwandiko.charAt(gukora_mu_matsinda_umugerekashakiro + 1) <= 0xdfff) 문자값 = 0x10000 + ((문자값 - 0xd800) << 10) + Umwandiko.charAt(++gukora_mu_matsinda_umugerekashakiro) - 0xdc00;
            else if (문자값 >= 0xd800 && 문자값 <= 0xdfff) 문자값 = '?';
            if (문자값 < 128) 임시[쓴수++] = (byte)문자값;
            else if (문자값 < 2048) { 임시[쓴수++] = (byte)(192 | 문자값 >> 6); 임시[쓴수++] = (byte)(128 | 문자값 & 63); }
            else if (문자값 < 65536) { 임시[쓴수++] = (byte)(224 | 문자값 >> 12); 임시[쓴수++] = (byte)(128 | 문자값 >> 6 & 63); 임시[쓴수++] = (byte)(128 | 문자값 & 63); }
            else { 임시[쓴수++] = (byte)(240 | 문자값 >> 18); 임시[쓴수++] = (byte)(128 | 문자값 >> 12 & 63); 임시[쓴수++] = (byte)(128 | 문자값 >> 6 & 63); 임시[쓴수++] = (byte)(128 | 문자값 & 63); }
        }
        byte[] 결과 = new byte[쓴수]; System.arraycopy(임시, 0, 결과, 0, 쓴수); return 결과;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String gusobanura_amakurushingiro(byte[] bayiti_agaciro) {
        StringBuilder 결과 = new StringBuilder();
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < bayiti_agaciro.length;) {
            int 문자값 = bayiti_agaciro[gukora_mu_matsinda_umugerekashakiro++] & 255, 수 = 문자값 < 128 ? 0 : 문자값 >= 194 && 문자값 < 224 ? 1 : 문자값 >= 224 && 문자값 < 240 ? 2 : 문자값 >= 240 && 문자값 <= 244 ? 3 : -1;
            if (수 < 0 || bayiti_agaciro.length - gukora_mu_matsinda_umugerekashakiro < 수) throw new 잘못된인수예외("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) 문자값 &= (1 << (6 - 수)) - 1;
            for (int 안쪽자리 = 0; 안쪽자리 < 수; 안쪽자리++) { int Ikibanza_agaciro = bayiti_agaciro[gukora_mu_matsinda_umugerekashakiro++] & 255; if ((Ikibanza_agaciro & 192) != 128) throw new 잘못된인수예외("잘못된 UTF-8"); 문자값 = 문자값 << 6 | Ikibanza_agaciro & 63; }
            if (문자값 < 최소 || 문자값 > 0x10ffff || 문자값 >= 0xd800 && 문자값 <= 0xdfff) throw new 잘못된인수예외("잘못된 UTF-8");
            if (문자값 < 65536) 결과.append((char)문자값);
            else { 문자값 -= 65536; 결과.append((char)(0xd800 | 문자값 >> 10)); 결과.append((char)(0xdc00 | 문자값 & 1023)); }
        }
        return 결과.toString();
    }
}
