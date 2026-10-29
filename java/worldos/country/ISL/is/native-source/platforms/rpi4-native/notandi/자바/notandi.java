// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 Verkfæri 전용 SVC Tengjast. 기존 x86 Verkfæri 원문을 함께 빌드한다. */
public final class notandi {
    public static native int 파일서술자열기(int[] Heiti, int Stillingar);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int VALUE);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] Heiti, int[] gögn);
    public static native int skrifa_skrá(int[] Heiti, int[] gögn, int lengd_VALUE);
    public static native int Skrift(String Texti);
    public static native int skrifa_stafur_VALUE(int VALUE);
    public static native int 인수개수();
    public static native String Viðföng(int INDEX);
    public static native int verkfæri_númer();
    public static native int 화면연결(int Aðgerð, int INDEX, int 가, int 나, int 다, int 라);
    public static native int 화면글(int INDEX, int[] Texti, int lengd_VALUE);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int Stream_stýring(int Aðgerð, int 서술자, int VALUE);
    public static native int TENGJA_Stream(int 서술자, int slóð, int gátt_VALUE);
    public static native int opið_Net(int gátt_VALUE);
    public static native int senda_Net(int 서술자, int slóð, int gátt_VALUE, int[] gögn, int lengd_VALUE);
    public static native int 통신받기(int 서술자, int[] gögn, int lengd_VALUE);
    public static native int Net_gátt(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int Lóðrétt_staða, int 폭, int 높이, int 색);
}
