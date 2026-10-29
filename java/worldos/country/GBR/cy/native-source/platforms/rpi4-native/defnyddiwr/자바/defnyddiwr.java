// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 Offer 전용 SVC Cysylltu. 기존 x86 Offer 원문을 함께 빌드한다. */
public final class defnyddiwr {
    public static native int 파일서술자열기(int[] Enw, int Gosodiadau);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int VALUE);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] Enw, int[] data);
    public static native int ysgrifennu_ffeil(int[] Enw, int[] data, int hyd_VALUE);
    public static native int Ysgrifennu(String Testun);
    public static native int ysgrifennu_nod_VALUE(int VALUE);
    public static native int 인수개수();
    public static native String 인수(int INDEX);
    public static native int 도구번호();
    public static native int 화면연결(int Gweithrediad, int INDEX, int 가, int 나, int 다, int 라);
    public static native int 화면글(int INDEX, int[] Testun, int hyd_VALUE);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int ffrwd_rheoli(int Gweithrediad, int 서술자, int VALUE);
    public static native int Cysylltu_ffrwd(int 서술자, int ADDRESS, int porth_VALUE);
    public static native int agor_Rhwydwaith(int porth_VALUE);
    public static native int anfon_Rhwydwaith(int 서술자, int ADDRESS, int porth_VALUE, int[] data, int hyd_VALUE);
    public static native int 통신받기(int 서술자, int[] data, int hyd_VALUE);
    public static native int Rhwydwaith_porth(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int Ar_i_fyny_safle, int 폭, int 높이, int 색);
}
