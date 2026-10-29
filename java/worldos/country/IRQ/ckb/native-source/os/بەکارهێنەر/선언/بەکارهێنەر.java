// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros بەکارهێنەر ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class بەکارهێنەر {
    public static native int 파일서술자열기(int[] فایل_تێنووسین_ناو, int کردنەوە_ڕێكبەندەكان);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int بایت_نرخ);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] ناو, int[] دەیتا);
    public static native int ڕایت_کردن_نووسە_نرخ(int 문자);
    public static native int ڕایت_کردن_فایل(int[] ناو, int[] دەیتا, int درێژی_نرخ);
    public static native int ڕایت_کردن(String ناوەرۆک_نرخ);
    public static native int 인수개수();
    public static native String 인수(int پێرست);
    public static native int 실행권한();
    public static native int کردنەوە_تۆڕ(int مەحەلی_دەرگا);
    public static native int ناردن_دەیتا(int دەسک_نرخ, int ناونیشان, int جێمەبەست_دەرگا, int[] دەیتا, int درێژی_نرخ);
    public static native int 자료받기(int دەسک_نرخ, int[] دەیتا, int 제한밀리초);
    public static native int داخستن_تۆڕ(int دەسک_نرخ);
    public static native int 내주소();
    public static native int 보낸주소(int دەسک_نرخ);
    public static native int 보낸창구(int دەسک_نرخ);
}
