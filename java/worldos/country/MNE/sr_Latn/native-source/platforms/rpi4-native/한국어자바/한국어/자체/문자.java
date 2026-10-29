// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 문자(文字), kodiranje_VALUE(符號): UTF-8 바이트와 UTF-16 문자열의 CONVERT_VALUE. normalizovati_VALUE/조합 입력기는 별개다. */
public final class 문자 {
    public static int bajt_COUNT(byte[] podaci) { return podaci.length; }
    private 문자() {}
    public static int 길이(String SMS) { return SMS.length(); }
    public static boolean 같음(String čeona_kamera_VALUE, String NAZAD_VALUE) { return čeona_kamera_VALUE == null ? NAZAD_VALUE == null : čeona_kamera_VALUE.equals(NAZAD_VALUE); }
    public static String nalepiti_SMS(String čeona_kamera_VALUE, String NAZAD_VALUE) { return čeona_kamera_VALUE.concat(NAZAD_VALUE); }
    public static String iseći_VALUE(String SMS, int koristiti, int 끝) { return SMS.substring(koristiti, 끝); }
    public static int raščlaniti_ceo_broj(String SMS) { try { return Integer.parseInt(SMS); } catch (NumberFormatException greška) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String 정수쓰기(int 수) { return Integer.toString(수); }
    public static int kôd_znaka_COUNT(String SMS) {
        int 수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < SMS.length(); Loop_INDEX++, 수++) {
            int kôd_znaka = SMS.charAt(Loop_INDEX);
            if (kôd_znaka >= 0xd800 && kôd_znaka <= 0xdbff && Loop_INDEX + 1 < SMS.length() && SMS.charAt(Loop_INDEX + 1) >= 0xdc00 && SMS.charAt(Loop_INDEX + 1) <= 0xdfff) Loop_INDEX++;
        }
        return 수;
    }
    public static byte[] kodirati(String SMS) {
        byte[] 임시 = new byte[SMS.length() * 3]; int 쓴수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < SMS.length(); Loop_INDEX++) {
            int kôd_znaka = SMS.charAt(Loop_INDEX);
            if (kôd_znaka >= 0xd800 && kôd_znaka <= 0xdbff && Loop_INDEX + 1 < SMS.length() && SMS.charAt(Loop_INDEX + 1) >= 0xdc00 && SMS.charAt(Loop_INDEX + 1) <= 0xdfff) kôd_znaka = 0x10000 + ((kôd_znaka - 0xd800) << 10) + SMS.charAt(++Loop_INDEX) - 0xdc00;
            else if (kôd_znaka >= 0xd800 && kôd_znaka <= 0xdfff) kôd_znaka = '?';
            if (kôd_znaka < 128) 임시[쓴수++] = (byte)kôd_znaka;
            else if (kôd_znaka < 2048) { 임시[쓴수++] = (byte)(192 | kôd_znaka >> 6); 임시[쓴수++] = (byte)(128 | kôd_znaka & 63); }
            else if (kôd_znaka < 65536) { 임시[쓴수++] = (byte)(224 | kôd_znaka >> 12); 임시[쓴수++] = (byte)(128 | kôd_znaka >> 6 & 63); 임시[쓴수++] = (byte)(128 | kôd_znaka & 63); }
            else { 임시[쓴수++] = (byte)(240 | kôd_znaka >> 18); 임시[쓴수++] = (byte)(128 | kôd_znaka >> 12 & 63); 임시[쓴수++] = (byte)(128 | kôd_znaka >> 6 & 63); 임시[쓴수++] = (byte)(128 | kôd_znaka & 63); }
        }
        byte[] KR = new byte[쓴수]; System.arraycopy(임시, 0, KR, 0, 쓴수); return KR;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String dešifrovati_podaci(byte[] bajt_VALUE) {
        StringBuilder KR = new StringBuilder();
        for (int Loop_INDEX = 0; Loop_INDEX < bajt_VALUE.length;) {
            int kôd_znaka = bajt_VALUE[Loop_INDEX++] & 255, 수 = kôd_znaka < 128 ? 0 : kôd_znaka >= 194 && kôd_znaka < 224 ? 1 : kôd_znaka >= 224 && kôd_znaka < 240 ? 2 : kôd_znaka >= 240 && kôd_znaka <= 244 ? 3 : -1;
            if (수 < 0 || bajt_VALUE.length - Loop_INDEX < 수) throw new nevažeći_argument_izuzetak("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) kôd_znaka &= (1 << (6 - 수)) - 1;
            for (int unutrašnje_pozicija = 0; unutrašnje_pozicija < 수; unutrašnje_pozicija++) { int NAZAD_VALUE = bajt_VALUE[Loop_INDEX++] & 255; if ((NAZAD_VALUE & 192) != 128) throw new nevažeći_argument_izuzetak("잘못된 UTF-8"); kôd_znaka = kôd_znaka << 6 | NAZAD_VALUE & 63; }
            if (kôd_znaka < 최소 || kôd_znaka > 0x10ffff || kôd_znaka >= 0xd800 && kôd_znaka <= 0xdfff) throw new nevažeći_argument_izuzetak("잘못된 UTF-8");
            if (kôd_znaka < 65536) KR.append((char)kôd_znaka);
            else { kôd_znaka -= 65536; KR.append((char)(0xd800 | kôd_znaka >> 10)); KR.append((char)(0xdc00 | kôd_znaka & 1023)); }
        }
        return KR.toString();
    }
}
