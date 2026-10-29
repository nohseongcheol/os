// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 innealan 전용 SVC CONNECT. 기존 x86 innealan 원문을 함께 빌드한다. */
public final class cleachdaiche {
    public static native int 파일서술자열기(int[] Ainm, int roghainnean);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int VALUE);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] Ainm, int[] dàta);
    public static native int sgrìobh_faidhle(int[] Ainm, int[] dàta, int faid_VALUE);
    public static native int sgrìobh(String SMS);
    public static native int sgrìobh_caractar_VALUE(int VALUE);
    public static native int 인수개수();
    public static native String 인수(int INDEX);
    public static native int 도구번호();
    public static native int 화면연결(int Gnìomh, int INDEX, int 가, int 나, int 다, int 라);
    public static native int 화면글(int INDEX, int[] SMS, int faid_VALUE);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int sruth_smachd(int Gnìomh, int 서술자, int VALUE);
    public static native int CONNECT_sruth(int 서술자, int ADDRESS, int port_VALUE);
    public static native int fosgail_lìonra(int port_VALUE);
    public static native int cuir_lìonra(int 서술자, int ADDRESS, int port_VALUE, int[] dàta, int faid_VALUE);
    public static native int 통신받기(int 서술자, int[] dàta, int faid_VALUE);
    public static native int lìonra_port(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int inghearach_suidhich, int 폭, int 높이, int 색);
}
