// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 문자(文字), ضابطہ_ربائی_قدر(符號): UTF-8 바이트와 UTF-16 문자열의 변환. عام_بناؤ_قدر/조합 입력기는 별개다. */
public final class 문자 {
    public static int 바이트수(byte[] کوائف) { return کوائف.length; }
    private 문자() {}
    public static int لمبائی_قدر(String متن) { return متن.length(); }
    public static boolean 같음(String 앞, String پیچھے_قدر) { return 앞 == null ? پیچھے_قدر == null : 앞.equals(پیچھے_قدر); }
    public static String جپکاؤ_متن(String 앞, String پیچھے_قدر) { return 앞.concat(پیچھے_قدر); }
    public static String کاٹو_قدر(String متن, int چلاؤ, int 끝) { return متن.substring(چلاؤ, 끝); }
    public static int 정수읽기(String متن) { try { return Integer.parseInt(متن); } catch (NumberFormatException نقص) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String لکھو_عدد_قدر(int 수) { return Integer.toString(수); }
    public static int 코드포인트수(String متن) {
        int 수 = 0;
        for (int لوپ_اشاریہ = 0; لوپ_اشاریہ < متن.length(); لوپ_اشاریہ++, 수++) {
            int کیریکٹر_کوڈ = متن.charAt(لوپ_اشاریہ);
            if (کیریکٹر_کوڈ >= 0xd800 && کیریکٹر_کوڈ <= 0xdbff && لوپ_اشاریہ + 1 < متن.length() && متن.charAt(لوپ_اشاریہ + 1) >= 0xdc00 && متن.charAt(لوپ_اشاریہ + 1) <= 0xdfff) لوپ_اشاریہ++;
        }
        return 수;
    }
    public static byte[] 부호화(String متن) {
        byte[] 임시 = new byte[متن.length() * 3]; int 쓴수 = 0;
        for (int لوپ_اشاریہ = 0; لوپ_اشاریہ < متن.length(); لوپ_اشاریہ++) {
            int کیریکٹر_کوڈ = متن.charAt(لوپ_اشاریہ);
            if (کیریکٹر_کوڈ >= 0xd800 && کیریکٹر_کوڈ <= 0xdbff && لوپ_اشاریہ + 1 < متن.length() && متن.charAt(لوپ_اشاریہ + 1) >= 0xdc00 && متن.charAt(لوپ_اشاریہ + 1) <= 0xdfff) کیریکٹر_کوڈ = 0x10000 + ((کیریکٹر_کوڈ - 0xd800) << 10) + متن.charAt(++لوپ_اشاریہ) - 0xdc00;
            else if (کیریکٹر_کوڈ >= 0xd800 && کیریکٹر_کوڈ <= 0xdfff) کیریکٹر_کوڈ = '?';
            if (کیریکٹر_کوڈ < 128) 임시[쓴수++] = (byte)کیریکٹر_کوڈ;
            else if (کیریکٹر_کوڈ < 2048) { 임시[쓴수++] = (byte)(192 | کیریکٹر_کوڈ >> 6); 임시[쓴수++] = (byte)(128 | کیریکٹر_کوڈ & 63); }
            else if (کیریکٹر_کوڈ < 65536) { 임시[쓴수++] = (byte)(224 | کیریکٹر_کوڈ >> 12); 임시[쓴수++] = (byte)(128 | کیریکٹر_کوڈ >> 6 & 63); 임시[쓴수++] = (byte)(128 | کیریکٹر_کوڈ & 63); }
            else { 임시[쓴수++] = (byte)(240 | کیریکٹر_کوڈ >> 18); 임시[쓴수++] = (byte)(128 | کیریکٹر_کوڈ >> 12 & 63); 임시[쓴수++] = (byte)(128 | کیریکٹر_کوڈ >> 6 & 63); 임시[쓴수++] = (byte)(128 | کیریکٹر_کوڈ & 63); }
        }
        byte[] 결과 = new byte[쓴수]; System.arraycopy(임시, 0, 결과, 0, 쓴수); return 결과;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String ضابطہ_کشائی_کرو_کوائف(byte[] بائٹ_قدر) {
        StringBuilder 결과 = new StringBuilder();
        for (int لوپ_اشاریہ = 0; لوپ_اشاریہ < بائٹ_قدر.length;) {
            int کیریکٹر_کوڈ = بائٹ_قدر[لوپ_اشاریہ++] & 255, 수 = کیریکٹر_کوڈ < 128 ? 0 : کیریکٹر_کوڈ >= 194 && کیریکٹر_کوڈ < 224 ? 1 : کیریکٹر_کوڈ >= 224 && کیریکٹر_کوڈ < 240 ? 2 : کیریکٹر_کوڈ >= 240 && کیریکٹر_کوڈ <= 244 ? 3 : -1;
            if (수 < 0 || بائٹ_قدر.length - لوپ_اشاریہ < 수) throw new 잘못된인수예외("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) کیریکٹر_کوڈ &= (1 << (6 - 수)) - 1;
            for (int 안쪽자리 = 0; 안쪽자리 < 수; 안쪽자리++) { int پیچھے_قدر = بائٹ_قدر[لوپ_اشاریہ++] & 255; if ((پیچھے_قدر & 192) != 128) throw new 잘못된인수예외("잘못된 UTF-8"); کیریکٹر_کوڈ = کیریکٹر_کوڈ << 6 | پیچھے_قدر & 63; }
            if (کیریکٹر_کوڈ < 최소 || کیریکٹر_کوڈ > 0x10ffff || کیریکٹر_کوڈ >= 0xd800 && کیریکٹر_کوڈ <= 0xdfff) throw new 잘못된인수예외("잘못된 UTF-8");
            if (کیریکٹر_کوڈ < 65536) 결과.append((char)کیریکٹر_کوڈ);
            else { کیریکٹر_کوڈ -= 65536; 결과.append((char)(0xd800 | کیریکٹر_کوڈ >> 10)); 결과.append((char)(0xdc00 | کیریکٹر_کوڈ & 1023)); }
        }
        return 결과.toString();
    }
}
