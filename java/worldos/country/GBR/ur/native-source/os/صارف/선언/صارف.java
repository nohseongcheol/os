// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros صارف ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class صارف {
    public static native int 파일서술자열기(int[] فائل_اندراج_نام, int بنائیں_سیٹنگز);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int بائٹ_قدر);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] نام, int[] کوائف);
    public static native int لکھیں_کریکٹر_قدر(int 문자);
    public static native int لکھیں_فائل(int[] نام, int[] کوائف, int لمبا_ئی_قدر);
    public static native int لکھیں(String مشمول_قدر);
    public static native int 인수개수();
    public static native String دلائل(int اشاریہ);
    public static native int 실행권한();
    public static native int بنائیں_نیٹ_ورک(int مقامی_پورٹ);
    public static native int بھیجیں_کوائف(int ہینڈل_قدر, int پتہ, int منزل_مقصود_پورٹ, int[] کوائف, int لمبا_ئی_قدر);
    public static native int 자료받기(int ہینڈل_قدر, int[] کوائف, int 제한밀리초);
    public static native int بند_نیٹ_ورک(int ہینڈل_قدر);
    public static native int 내주소();
    public static native int 보낸주소(int ہینڈل_قدر);
    public static native int 보낸창구(int ہینڈل_قدر);
}
