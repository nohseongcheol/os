// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros defnyddiwr ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class defnyddiwr {
    public static native int 파일서술자열기(int[] ffeil_cofnod_enw, int agor_Gosodiadau);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int beit_VALUE);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] Enw, int[] data);
    public static native int ysgrifennu_nod_VALUE(int 문자);
    public static native int ysgrifennu_ffeil(int[] Enw, int[] data, int hyd_VALUE);
    public static native int Ysgrifennu(String Cynnwys_VALUE);
    public static native int 인수개수();
    public static native String 인수(int INDEX);
    public static native int 실행권한();
    public static native int agor_Rhwydwaith(int lleol_porth);
    public static native int anfon_data(int dolen_VALUE, int ADDRESS, int cyrchfan_porth, int[] data, int hyd_VALUE);
    public static native int 자료받기(int dolen_VALUE, int[] data, int 제한밀리초);
    public static native int cau_Rhwydwaith(int dolen_VALUE);
    public static native int 내주소();
    public static native int 보낸주소(int dolen_VALUE);
    public static native int 보낸창구(int dolen_VALUE);
}
