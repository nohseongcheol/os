// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros korisnik ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class korisnik {
    public static native int 파일서술자열기(int[] fajl_unos_naziv, int kreirati_Postavke);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int bajt_VALUE);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] Naziv, int[] podaci);
    public static native int pisati_znak_VALUE(int 문자);
    public static native int pisati_fajl(int[] Naziv, int[] podaci, int dužina_VALUE);
    public static native int Piši(String Sadržaj_VALUE);
    public static native int 인수개수();
    public static native String Argumenti(int INDEX);
    public static native int 실행권한();
    public static native int kreirati_Mreža(int lokalni_port);
    public static native int poslati_podaci(int hvatište_VALUE, int adresa, int odredište_port, int[] podaci, int dužina_VALUE);
    public static native int 자료받기(int hvatište_VALUE, int[] podaci, int 제한밀리초);
    public static native int zatvoriti_Mreža(int hvatište_VALUE);
    public static native int 내주소();
    public static native int 보낸주소(int hvatište_VALUE);
    public static native int 보낸창구(int hvatište_VALUE);
}
