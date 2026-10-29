// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros gebruiker ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class gebruiker {
    public static native int 파일서술자열기(int[] lêer_inskrywing_naam, int skep_Instellings);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int greep_VALUE);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] Naam, int[] data);
    public static native int skryf_karakter_VALUE(int 문자);
    public static native int skryf_lêer(int[] Naam, int[] data, int lengte_VALUE);
    public static native int Skryf(String Inhoud_VALUE);
    public static native int 인수개수();
    public static native String 인수(int INDEX);
    public static native int 실행권한();
    public static native int skep_Netwerk(int lokaal_ombou);
    public static native int e_pos_data(int handvatsel_VALUE, int adres, int bestemming_ombou, int[] data, int lengte_VALUE);
    public static native int 자료받기(int handvatsel_VALUE, int[] data, int 제한밀리초);
    public static native int sluit_Netwerk(int handvatsel_VALUE);
    public static native int 내주소();
    public static native int 보낸주소(int handvatsel_VALUE);
    public static native int 보낸창구(int handvatsel_VALUE);
}
