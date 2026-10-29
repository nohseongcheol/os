// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 문자(文字), نهێنبەندی_نرخ(符號): UTF-8 바이트와 UTF-16 문자열의 변환. ئاساییکردن_نرخ/조합 입력기는 별개다. */
public final class 문자 {
    public static int 바이트수(byte[] دەیتا) { return دەیتا.length; }
    private 문자() {}
    public static int درێژی_نرخ(String دەق) { return دەق.length(); }
    public static boolean 같음(String 앞, String دواوە_نرخ) { return 앞 == null ? دواوە_نرخ == null : 앞.equals(دواوە_نرخ); }
    public static String چەسپاندن_دەق(String 앞, String دواوە_نرخ) { return 앞.concat(دواوە_نرخ); }
    public static String بڕین_نرخ(String دەق, int ڕادان, int 끝) { return دەق.substring(ڕادان, 끝); }
    public static int 정수읽기(String دەق) { try { return Integer.parseInt(دەق); } catch (NumberFormatException هەڵە) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String ڕایت_کردن_ژمارەی_سروشتی_نرخ(int 수) { return Integer.toString(수); }
    public static int 코드포인트수(String دەق) {
        int 수 = 0;
        for (int گێژەن_پێرست = 0; گێژەن_پێرست < دەق.length(); گێژەن_پێرست++, 수++) {
            int کۆدی_نووسە = دەق.charAt(گێژەن_پێرست);
            if (کۆدی_نووسە >= 0xd800 && کۆدی_نووسە <= 0xdbff && گێژەن_پێرست + 1 < دەق.length() && دەق.charAt(گێژەن_پێرست + 1) >= 0xdc00 && دەق.charAt(گێژەن_پێرست + 1) <= 0xdfff) گێژەن_پێرست++;
        }
        return 수;
    }
    public static byte[] 부호화(String دەق) {
        byte[] 임시 = new byte[دەق.length() * 3]; int 쓴수 = 0;
        for (int گێژەن_پێرست = 0; گێژەن_پێرست < دەق.length(); گێژەن_پێرست++) {
            int کۆدی_نووسە = دەق.charAt(گێژەن_پێرست);
            if (کۆدی_نووسە >= 0xd800 && کۆدی_نووسە <= 0xdbff && گێژەن_پێرست + 1 < دەق.length() && دەق.charAt(گێژەن_پێرست + 1) >= 0xdc00 && دەق.charAt(گێژەن_پێرست + 1) <= 0xdfff) کۆدی_نووسە = 0x10000 + ((کۆدی_نووسە - 0xd800) << 10) + دەق.charAt(++گێژەن_پێرست) - 0xdc00;
            else if (کۆدی_نووسە >= 0xd800 && کۆدی_نووسە <= 0xdfff) کۆدی_نووسە = '?';
            if (کۆدی_نووسە < 128) 임시[쓴수++] = (byte)کۆدی_نووسە;
            else if (کۆدی_نووسە < 2048) { 임시[쓴수++] = (byte)(192 | کۆدی_نووسە >> 6); 임시[쓴수++] = (byte)(128 | کۆدی_نووسە & 63); }
            else if (کۆدی_نووسە < 65536) { 임시[쓴수++] = (byte)(224 | کۆدی_نووسە >> 12); 임시[쓴수++] = (byte)(128 | کۆدی_نووسە >> 6 & 63); 임시[쓴수++] = (byte)(128 | کۆدی_نووسە & 63); }
            else { 임시[쓴수++] = (byte)(240 | کۆدی_نووسە >> 18); 임시[쓴수++] = (byte)(128 | کۆدی_نووسە >> 12 & 63); 임시[쓴수++] = (byte)(128 | کۆدی_نووسە >> 6 & 63); 임시[쓴수++] = (byte)(128 | کۆدی_نووسە & 63); }
        }
        byte[] 결과 = new byte[쓴수]; System.arraycopy(임시, 0, 결과, 0, 쓴수); return 결과;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String بێڕەمز_کردن_دەیتا(byte[] بایت_نرخ) {
        StringBuilder 결과 = new StringBuilder();
        for (int گێژەن_پێرست = 0; گێژەن_پێرست < بایت_نرخ.length;) {
            int کۆدی_نووسە = بایت_نرخ[گێژەن_پێرست++] & 255, 수 = کۆدی_نووسە < 128 ? 0 : کۆدی_نووسە >= 194 && کۆدی_نووسە < 224 ? 1 : کۆدی_نووسە >= 224 && کۆدی_نووسە < 240 ? 2 : کۆدی_نووسە >= 240 && کۆدی_نووسە <= 244 ? 3 : -1;
            if (수 < 0 || بایت_نرخ.length - گێژەن_پێرست < 수) throw new 잘못된인수예외("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) کۆدی_نووسە &= (1 << (6 - 수)) - 1;
            for (int 안쪽자리 = 0; 안쪽자리 < 수; 안쪽자리++) { int دواوە_نرخ = بایت_نرخ[گێژەن_پێرست++] & 255; if ((دواوە_نرخ & 192) != 128) throw new 잘못된인수예외("잘못된 UTF-8"); کۆدی_نووسە = کۆدی_نووسە << 6 | دواوە_نرخ & 63; }
            if (کۆدی_نووسە < 최소 || کۆدی_نووسە > 0x10ffff || کۆدی_نووسە >= 0xd800 && کۆدی_نووسە <= 0xdfff) throw new 잘못된인수예외("잘못된 UTF-8");
            if (کۆدی_نووسە < 65536) 결과.append((char)کۆدی_نووسە);
            else { کۆدی_نووسە -= 65536; 결과.append((char)(0xd800 | کۆدی_نووسە >> 10)); 결과.append((char)(0xdc00 | کۆدی_نووسە & 1023)); }
        }
        return 결과.toString();
    }
}
