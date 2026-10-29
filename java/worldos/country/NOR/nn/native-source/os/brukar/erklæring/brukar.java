// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros brukar ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class brukar {
    public static native int 파일서술자열기(int[] fil_oppføring_namn, int opne_Innstillingar);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int byte_VALUE);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] Namn, int[] data);
    public static native int skrive_teikn_VALUE(int 문자);
    public static native int skrive_fil(int[] Namn, int[] data, int lengd_VALUE);
    public static native int Skriv(String Innhald_VALUE);
    public static native int 인수개수();
    public static native String Argument(int INDEX);
    public static native int 실행권한();
    public static native int opne_Nettverk(int lokal_port);
    public static native int sende_data(int handtak_VALUE, int ADDRESS, int mål_port, int[] data, int lengd_VALUE);
    public static native int 자료받기(int handtak_VALUE, int[] data, int 제한밀리초);
    public static native int Lukk_Nettverk(int handtak_VALUE);
    public static native int 내주소();
    public static native int 보낸주소(int handtak_VALUE);
    public static native int 보낸창구(int handtak_VALUE);
}
