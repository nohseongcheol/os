// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 Mga_Tool 전용 SVC CONNECT. 기존 x86 Mga_Tool 원문을 함께 빌드한다. */
public final class gumagamit {
    public static native int 파일서술자열기(int[] pangalan, int Mga_Setting);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int VALUE);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] pangalan, int[] data);
    public static native int sumulat_file(int[] pangalan, int[] data, int haba_VALUE);
    public static native int sumulat(String SMS);
    public static native int sumulat_karakter_VALUE(int VALUE);
    public static native int 인수개수();
    public static native String 인수(int INDEX);
    public static native int 도구번호();
    public static native int 화면연결(int aksyon, int INDEX, int 가, int 나, int 다, int 라);
    public static native int 화면글(int INDEX, int[] SMS, int haba_VALUE);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int Stream_control(int aksyon, int 서술자, int VALUE);
    public static native int CONNECT_Stream(int 서술자, int email, int port_VALUE);
    public static native int buksan_Network(int port_VALUE);
    public static native int i_email_Network(int 서술자, int email, int port_VALUE, int[] data, int haba_VALUE);
    public static native int 통신받기(int 서술자, int[] data, int haba_VALUE);
    public static native int Network_port(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int archive_posisyon, int 폭, int 높이, int 색);
}
