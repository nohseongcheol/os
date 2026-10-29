// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 문자(文字), dokkagol_njaru(符號): UTF-8 바이트와 UTF-16 문자열의 변환. 정규화/조합 입력기는 별개다. */
public final class 문자 {
    public static int 바이트수(byte[] keɓe) { return keɓe.length; }
    private 문자() {}
    public static int njuuteendi_njaru(String binndi) { return binndi.length(); }
    public static boolean 같음(String 앞, String Caggal_njaru) { return 앞 == null ? Caggal_njaru == null : 앞.equals(Caggal_njaru); }
    public static String ɗakkude_binndi(String 앞, String Caggal_njaru) { return 앞.concat(Caggal_njaru); }
    public static String taƴde_njaru(String binndi, int huutoraade, int 끝) { return binndi.substring(huutoraade, 끝); }
    public static int 정수읽기(String binndi) { try { return Integer.parseInt(binndi); } catch (NumberFormatException juumre) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String 정수쓰기(int 수) { return Integer.toString(수); }
    public static int 코드포인트수(String binndi) {
        int 수 = 0;
        for (int kowal_joopirdu = 0; kowal_joopirdu < binndi.length(); kowal_joopirdu++, 수++) {
            int 문자값 = binndi.charAt(kowal_joopirdu);
            if (문자값 >= 0xd800 && 문자값 <= 0xdbff && kowal_joopirdu + 1 < binndi.length() && binndi.charAt(kowal_joopirdu + 1) >= 0xdc00 && binndi.charAt(kowal_joopirdu + 1) <= 0xdfff) kowal_joopirdu++;
        }
        return 수;
    }
    public static byte[] 부호화(String binndi) {
        byte[] 임시 = new byte[binndi.length() * 3]; int 쓴수 = 0;
        for (int kowal_joopirdu = 0; kowal_joopirdu < binndi.length(); kowal_joopirdu++) {
            int 문자값 = binndi.charAt(kowal_joopirdu);
            if (문자값 >= 0xd800 && 문자값 <= 0xdbff && kowal_joopirdu + 1 < binndi.length() && binndi.charAt(kowal_joopirdu + 1) >= 0xdc00 && binndi.charAt(kowal_joopirdu + 1) <= 0xdfff) 문자값 = 0x10000 + ((문자값 - 0xd800) << 10) + binndi.charAt(++kowal_joopirdu) - 0xdc00;
            else if (문자값 >= 0xd800 && 문자값 <= 0xdfff) 문자값 = '?';
            if (문자값 < 128) 임시[쓴수++] = (byte)문자값;
            else if (문자값 < 2048) { 임시[쓴수++] = (byte)(192 | 문자값 >> 6); 임시[쓴수++] = (byte)(128 | 문자값 & 63); }
            else if (문자값 < 65536) { 임시[쓴수++] = (byte)(224 | 문자값 >> 12); 임시[쓴수++] = (byte)(128 | 문자값 >> 6 & 63); 임시[쓴수++] = (byte)(128 | 문자값 & 63); }
            else { 임시[쓴수++] = (byte)(240 | 문자값 >> 18); 임시[쓴수++] = (byte)(128 | 문자값 >> 12 & 63); 임시[쓴수++] = (byte)(128 | 문자값 >> 6 & 63); 임시[쓴수++] = (byte)(128 | 문자값 & 63); }
        }
        byte[] 결과 = new byte[쓴수]; System.arraycopy(임시, 0, 결과, 0, 쓴수); return 결과;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String dokkitde_keɓe(byte[] oktee_njaru) {
        StringBuilder 결과 = new StringBuilder();
        for (int kowal_joopirdu = 0; kowal_joopirdu < oktee_njaru.length;) {
            int 문자값 = oktee_njaru[kowal_joopirdu++] & 255, 수 = 문자값 < 128 ? 0 : 문자값 >= 194 && 문자값 < 224 ? 1 : 문자값 >= 224 && 문자값 < 240 ? 2 : 문자값 >= 240 && 문자값 <= 244 ? 3 : -1;
            if (수 < 0 || oktee_njaru.length - kowal_joopirdu < 수) throw new 잘못된인수예외("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) 문자값 &= (1 << (6 - 수)) - 1;
            for (int 안쪽자리 = 0; 안쪽자리 < 수; 안쪽자리++) { int Caggal_njaru = oktee_njaru[kowal_joopirdu++] & 255; if ((Caggal_njaru & 192) != 128) throw new 잘못된인수예외("잘못된 UTF-8"); 문자값 = 문자값 << 6 | Caggal_njaru & 63; }
            if (문자값 < 최소 || 문자값 > 0x10ffff || 문자값 >= 0xd800 && 문자값 <= 0xdfff) throw new 잘못된인수예외("잘못된 UTF-8");
            if (문자값 < 65536) 결과.append((char)문자값);
            else { 문자값 -= 65536; 결과.append((char)(0xd800 | 문자값 >> 10)); 결과.append((char)(0xdc00 | 문자값 & 1023)); }
        }
        return 결과.toString();
    }
}
