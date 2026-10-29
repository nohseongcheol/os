// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 ئامرازەکان 전용 SVC لكاندن. 기존 x86 ئامرازەکان 원문을 함께 빌드한다. */
public final class بەکارهێنەر {
    public static native int 파일서술자열기(int[] ناو, int ڕێكبەندەكان);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int نرخ);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] ناو, int[] دەیتا);
    public static native int ڕایت_کردن_فایل(int[] ناو, int[] دەیتا, int درێژی_نرخ);
    public static native int ڕایت_کردن(String دەق);
    public static native int ڕایت_کردن_نووسە_نرخ(int نرخ);
    public static native int 인수개수();
    public static native String 인수(int پێرست);
    public static native int 도구번호();
    public static native int 화면연결(int ئاکشن, int پێرست, int 가, int 나, int 다, int 라);
    public static native int 화면글(int پێرست, int[] دەق, int درێژی_نرخ);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int Stream_کۆنترۆڵ(int ئاکشن, int 서술자, int نرخ);
    public static native int لكاندن_Stream(int 서술자, int ناونیشان, int دەرگا_نرخ);
    public static native int کردنەوە_تۆڕ(int دەرگا_نرخ);
    public static native int ناردن_تۆڕ(int 서술자, int ناونیشان, int دەرگا_نرخ, int[] دەیتا, int درێژی_نرخ);
    public static native int 통신받기(int 서술자, int[] دەیتا, int درێژی_نرخ);
    public static native int تۆڕ_دەرگا(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int 세로, int 폭, int 높이, int 색);
}
