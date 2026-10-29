// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros utent ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class utent {
    public static native int 파일서술자열기(int[] fajl_entrata_isem, int fetaħ_Settings);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int byte_VALUE);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] isem, int[] data);
    public static native int kiteb_karattru_VALUE(int 문자);
    public static native int kiteb_fajl(int[] isem, int[] data, int tul_VALUE);
    public static native int kiteb(String Kontenut_VALUE);
    public static native int 인수개수();
    public static native String 인수(int INDEX);
    public static native int 실행권한();
    public static native int fetaħ_netwerk(int lokali_port);
    public static native int bagħat_data(int handle_VALUE, int ADDRESS, int destinazzjoni_port, int[] data, int tul_VALUE);
    public static native int 자료받기(int handle_VALUE, int[] data, int 제한밀리초);
    public static native int agħlaq_netwerk(int handle_VALUE);
    public static native int 내주소();
    public static native int 보낸주소(int handle_VALUE);
    public static native int 보낸창구(int handle_VALUE);
}
