// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros úsáideoir ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class úsáideoir {
    public static native int 파일서술자열기(int[] comhad_iontráil_ainm, int oscail_Socruithe);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int beart_VALUE);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] Ainm, int[] sonraí);
    public static native int scríobh_carachtar_VALUE(int 문자);
    public static native int scríobh_comhad(int[] Ainm, int[] sonraí, int fad_VALUE);
    public static native int Scríobh(String Inneachar_VALUE);
    public static native int 인수개수();
    public static native String Argóintí(int INDEX);
    public static native int 실행권한();
    public static native int oscail_Líonra(int logánta_port);
    public static native int seol_sonraí(int hanla_VALUE, int ADDRESS, int sprioc_port, int[] sonraí, int fad_VALUE);
    public static native int 자료받기(int hanla_VALUE, int[] sonraí, int 제한밀리초);
    public static native int dún_Líonra(int hanla_VALUE);
    public static native int 내주소();
    public static native int 보낸주소(int hanla_VALUE);
    public static native int 보낸창구(int hanla_VALUE);
}
