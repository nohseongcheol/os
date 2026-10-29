// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 Uirlisí 전용 SVC Nasc. 기존 x86 Uirlisí 원문을 함께 빌드한다. */
public final class úsáideoir {
    public static native int 파일서술자열기(int[] Ainm, int Socruithe);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int VALUE);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] Ainm, int[] sonraí);
    public static native int scríobh_comhad(int[] Ainm, int[] sonraí, int fad_VALUE);
    public static native int Scríobh(String Téacs);
    public static native int scríobh_carachtar_VALUE(int VALUE);
    public static native int 인수개수();
    public static native String Argóintí(int INDEX);
    public static native int 도구번호();
    public static native int 화면연결(int Gníomh, int INDEX, int 가, int 나, int 다, int 라);
    public static native int 화면글(int INDEX, int[] Téacs, int fad_VALUE);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int sruth_rialú(int Gníomh, int 서술자, int VALUE);
    public static native int nasc_sruth(int 서술자, int ADDRESS, int port_VALUE);
    public static native int oscail_Líonra(int port_VALUE);
    public static native int seol_Líonra(int 서술자, int ADDRESS, int port_VALUE, int[] sonraí, int fad_VALUE);
    public static native int 통신받기(int 서술자, int[] sonraí, int fad_VALUE);
    public static native int Líonra_port(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int Ingearach_suíomh, int 폭, int 높이, int 색);
}
