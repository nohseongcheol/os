// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros ئىشلەتكۈچى ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class ئىشلەتكۈچى {
    public static native int 파일서술자열기(int[] ھۆججەت_كىرگۈزۈش_نامى, int قۇرۇش_تەڭشەك);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int بايت_قىممىتى);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] ئاتى, int[] مەلۇمات);
    public static native int يازماق_ھەرپ_بەلگە_قىممىتى(int 문자);
    public static native int يازماق_ھۆججەت(int[] ئاتى, int[] مەلۇمات, int ئۇزۇنلۇق_قىممىتى);
    public static native int ياز(String مەزمۇن_قىممىتى);
    public static native int 인수개수();
    public static native String ئۆزگەرگۈچىلەر(int ئىندېكس);
    public static native int 실행권한();
    public static native int قۇرۇش_تور(int يەرلىك_ئېغىز);
    public static native int ئەۋەتمەك_مەلۇمات(int تۇتقۇچ_قىممىتى, int ئادرېس, int نىشان_ئېغىز, int[] مەلۇمات, int ئۇزۇنلۇق_قىممىتى);
    public static native int 자료받기(int تۇتقۇچ_قىممىتى, int[] مەلۇمات, int 제한밀리초);
    public static native int ئاياغ_تور(int تۇتقۇچ_قىممىتى);
    public static native int 내주소();
    public static native int 보낸주소(int تۇتقۇچ_قىممىتى);
    public static native int 보낸창구(int تۇتقۇچ_قىممىتى);
}
