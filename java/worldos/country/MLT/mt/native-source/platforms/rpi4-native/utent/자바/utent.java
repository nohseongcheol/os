// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 Għodod 전용 SVC AQBAD. 기존 x86 Għodod 원문을 함께 빌드한다. */
public final class utent {
    public static native int 파일서술자열기(int[] isem, int Settings);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int VALUE);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] isem, int[] data);
    public static native int kiteb_fajl(int[] isem, int[] data, int tul_VALUE);
    public static native int kiteb(String SMS);
    public static native int kiteb_karattru_VALUE(int VALUE);
    public static native int 인수개수();
    public static native String 인수(int INDEX);
    public static native int 도구번호();
    public static native int 화면연결(int azzjoni, int INDEX, int 가, int 나, int 다, int 라);
    public static native int 화면글(int INDEX, int[] SMS, int tul_VALUE);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int Stream_kontroll(int azzjoni, int 서술자, int VALUE);
    public static native int AQBAD_Stream(int 서술자, int ADDRESS, int port_VALUE);
    public static native int fetaħ_netwerk(int port_VALUE);
    public static native int bagħat_netwerk(int 서술자, int ADDRESS, int port_VALUE, int[] data, int tul_VALUE);
    public static native int 통신받기(int 서술자, int[] data, int tul_VALUE);
    public static native int netwerk_port(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int Vertikali_pożizzjoni, int 폭, int 높이, int 색);
}
