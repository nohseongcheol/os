// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 문자(文字), ضابطه_ربائي_قدر(符號): UTF-8 바이트와 UTF-16 문자열의 변환. عام_ڪرڻ_قدر/조합 입력기는 별개다. */
public final class 문자 {
    public static int 바이트수(byte[] ڪوائف) { return ڪوائف.length; }
    private 문자() {}
    public static int لمبائي_قدر(String متن) { return متن.length(); }
    public static boolean 같음(String 앞, String واپس_قدر) { return 앞 == null ? واپس_قدر == null : 앞.equals(واپس_قدر); }
    public static String چپڪايو_متن(String 앞, String واپس_قدر) { return 앞.concat(واپس_قدر); }
    public static String ڪٽيو_قدر(String متن, int هلائڻ, int 끝) { return متن.substring(هلائڻ, 끝); }
    public static int 정수읽기(String متن) { try { return Integer.parseInt(متن); } catch (NumberFormatException نقص) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String لکو_عدد_صحيح_قدر(int 수) { return Integer.toString(수); }
    public static int 코드포인트수(String متن) {
        int 수 = 0;
        for (int لوپ_ابتدائي = 0; لوپ_ابتدائي < متن.length(); لوپ_ابتدائي++, 수++) {
            int ڪئريڪٽر_ڪوڊ = متن.charAt(لوپ_ابتدائي);
            if (ڪئريڪٽر_ڪوڊ >= 0xd800 && ڪئريڪٽر_ڪوڊ <= 0xdbff && لوپ_ابتدائي + 1 < متن.length() && متن.charAt(لوپ_ابتدائي + 1) >= 0xdc00 && متن.charAt(لوپ_ابتدائي + 1) <= 0xdfff) لوپ_ابتدائي++;
        }
        return 수;
    }
    public static byte[] 부호화(String متن) {
        byte[] 임시 = new byte[متن.length() * 3]; int 쓴수 = 0;
        for (int لوپ_ابتدائي = 0; لوپ_ابتدائي < متن.length(); لوپ_ابتدائي++) {
            int ڪئريڪٽر_ڪوڊ = متن.charAt(لوپ_ابتدائي);
            if (ڪئريڪٽر_ڪوڊ >= 0xd800 && ڪئريڪٽر_ڪوڊ <= 0xdbff && لوپ_ابتدائي + 1 < متن.length() && متن.charAt(لوپ_ابتدائي + 1) >= 0xdc00 && متن.charAt(لوپ_ابتدائي + 1) <= 0xdfff) ڪئريڪٽر_ڪوڊ = 0x10000 + ((ڪئريڪٽر_ڪوڊ - 0xd800) << 10) + متن.charAt(++لوپ_ابتدائي) - 0xdc00;
            else if (ڪئريڪٽر_ڪوڊ >= 0xd800 && ڪئريڪٽر_ڪوڊ <= 0xdfff) ڪئريڪٽر_ڪوڊ = '?';
            if (ڪئريڪٽر_ڪوڊ < 128) 임시[쓴수++] = (byte)ڪئريڪٽر_ڪوڊ;
            else if (ڪئريڪٽر_ڪوڊ < 2048) { 임시[쓴수++] = (byte)(192 | ڪئريڪٽر_ڪوڊ >> 6); 임시[쓴수++] = (byte)(128 | ڪئريڪٽر_ڪوڊ & 63); }
            else if (ڪئريڪٽر_ڪوڊ < 65536) { 임시[쓴수++] = (byte)(224 | ڪئريڪٽر_ڪوڊ >> 12); 임시[쓴수++] = (byte)(128 | ڪئريڪٽر_ڪوڊ >> 6 & 63); 임시[쓴수++] = (byte)(128 | ڪئريڪٽر_ڪوڊ & 63); }
            else { 임시[쓴수++] = (byte)(240 | ڪئريڪٽر_ڪوڊ >> 18); 임시[쓴수++] = (byte)(128 | ڪئريڪٽر_ڪوڊ >> 12 & 63); 임시[쓴수++] = (byte)(128 | ڪئريڪٽر_ڪوڊ >> 6 & 63); 임시[쓴수++] = (byte)(128 | ڪئريڪٽر_ڪوڊ & 63); }
        }
        byte[] 결과 = new byte[쓴수]; System.arraycopy(임시, 0, 결과, 0, 쓴수); return 결과;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String طئي_ٿيل_ڪوائف(byte[] بائٽ_قدر) {
        StringBuilder 결과 = new StringBuilder();
        for (int لوپ_ابتدائي = 0; لوپ_ابتدائي < بائٽ_قدر.length;) {
            int ڪئريڪٽر_ڪوڊ = بائٽ_قدر[لوپ_ابتدائي++] & 255, 수 = ڪئريڪٽر_ڪوڊ < 128 ? 0 : ڪئريڪٽر_ڪوڊ >= 194 && ڪئريڪٽر_ڪوڊ < 224 ? 1 : ڪئريڪٽر_ڪوڊ >= 224 && ڪئريڪٽر_ڪوڊ < 240 ? 2 : ڪئريڪٽر_ڪوڊ >= 240 && ڪئريڪٽر_ڪوڊ <= 244 ? 3 : -1;
            if (수 < 0 || بائٽ_قدر.length - لوپ_ابتدائي < 수) throw new 잘못된인수예외("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) ڪئريڪٽر_ڪوڊ &= (1 << (6 - 수)) - 1;
            for (int 안쪽자리 = 0; 안쪽자리 < 수; 안쪽자리++) { int واپس_قدر = بائٽ_قدر[لوپ_ابتدائي++] & 255; if ((واپس_قدر & 192) != 128) throw new 잘못된인수예외("잘못된 UTF-8"); ڪئريڪٽر_ڪوڊ = ڪئريڪٽر_ڪوڊ << 6 | واپس_قدر & 63; }
            if (ڪئريڪٽر_ڪوڊ < 최소 || ڪئريڪٽر_ڪوڊ > 0x10ffff || ڪئريڪٽر_ڪوڊ >= 0xd800 && ڪئريڪٽر_ڪوڊ <= 0xdfff) throw new 잘못된인수예외("잘못된 UTF-8");
            if (ڪئريڪٽر_ڪوڊ < 65536) 결과.append((char)ڪئريڪٽر_ڪوڊ);
            else { ڪئريڪٽر_ڪوڊ -= 65536; 결과.append((char)(0xd800 | ڪئريڪٽر_ڪوڊ >> 10)); 결과.append((char)(0xdc00 | ڪئريڪٽر_ڪوڊ & 1023)); }
        }
        return 결과.toString();
    }
}
