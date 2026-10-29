// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 قوراللار 전용 SVC ئۇلا. 기존 x86 قوراللار 원문을 함께 빌드한다. */
public final class ئىشلەتكۈچى {
    public static native int 파일서술자열기(int[] ئاتى, int تەڭشەكلەر);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int قىممىتى);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] ئاتى, int[] مەلۇمات);
    public static native int يازماق_ھۆججەت(int[] ئاتى, int[] مەلۇمات, int ئۇزۇنلۇق_قىممىتى);
    public static native int ياز(String تېكىست);
    public static native int يازماق_ھەرپ_بەلگە_قىممىتى(int قىممىتى);
    public static native int 인수개수();
    public static native String ئۆزگەرگۈچىلەر(int ئىندېكس);
    public static native int 도구번호();
    public static native int 화면연결(int مەشغۇلات, int ئىندېكس, int 가, int 나, int 다, int 라);
    public static native int 화면글(int ئىندېكس, int[] تېكىست, int ئۇزۇنلۇق_قىممىتى);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int ئېقىم_كونترول(int مەشغۇلات, int 서술자, int قىممىتى);
    public static native int ئۇلاش_ئېقىم(int 서술자, int ئادرېس, int ئېغىز_قىممىتى);
    public static native int قۇرۇش_تور(int ئېغىز_قىممىتى);
    public static native int ئەۋەتمەك_تور(int 서술자, int ئادرېس, int ئېغىز_قىممىتى, int[] مەلۇمات, int ئۇزۇنلۇق_قىممىتى);
    public static native int 통신받기(int 서술자, int[] مەلۇمات, int ئۇزۇنلۇق_قىممىتى);
    public static native int تور_ئېغىز(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int تىك_ئورۇنلاشتۇرۇش, int 폭, int 높이, int 색);
}
