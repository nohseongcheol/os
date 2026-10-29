// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros kasutaja ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class kasutaja {
    public static native int 파일서술자열기(int[] Fail_kirje_nimetus, int avama_Sätted);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int bait_VALUE);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int kinnitamine_failisalvestusruum(int 파일서술자);
    public static native int 파일읽기(int[] Nimi_2, int[] andmed);
    public static native int kirjutamine_märk_VALUE(int 문자);
    public static native int kirjutamine_Fail(int[] Nimi_2, int[] andmed, int 길이);
    public static native int Kirjutamine(String Sisu_VALUE);
    public static native int 인수개수();
    public static native String Argumendid(int INDEX);
    public static native int 실행권한();
    public static native int avama_võrk(int kohalik_port);
    public static native int saatma_andmed(int pide_VALUE, int ADDRESS, int sihtkoht_port, int[] andmed, int 길이);
    public static native int saama_andmed(int pide_VALUE, int[] andmed, int 제한밀리초);
    public static native int Sule_võrk(int pide_VALUE);
    public static native int 내주소();
    public static native int 보낸주소(int pide_VALUE);
    public static native int 보낸창구(int pide_VALUE);
}
