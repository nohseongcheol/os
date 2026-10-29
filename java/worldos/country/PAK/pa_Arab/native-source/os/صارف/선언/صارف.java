// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros صارف ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class صارف {
    public static native int 파일서술자열기(int[] فائل_داخلہ_ناں, int بنڑاؤ_سیٹنگاں);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int بائٹ_قدر);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] ناں, int[] کوائف);
    public static native int لکھو_کریکٹر_قدر(int 문자);
    public static native int لکھو_فائل(int[] ناں, int[] کوائف, int لمبائی_قدر);
    public static native int لکھو(String اجزاء_قدر);
    public static native int 인수개수();
    public static native String 인수(int اشاریہ);
    public static native int 실행권한();
    public static native int بنڑاؤ_نیٹ_ورک(int مقامی_دہانہ);
    public static native int بھیجو_کوائف(int نبٹنا_قدر, int پتا, int منزل_مقصود_دہانہ, int[] کوائف, int لمبائی_قدر);
    public static native int 자료받기(int نبٹنا_قدر, int[] کوائف, int 제한밀리초);
    public static native int بند_کرو_نیٹ_ورک(int نبٹنا_قدر);
    public static native int 내주소();
    public static native int 보낸주소(int نبٹنا_قدر);
    public static native int 보낸창구(int نبٹنا_قدر);
}
