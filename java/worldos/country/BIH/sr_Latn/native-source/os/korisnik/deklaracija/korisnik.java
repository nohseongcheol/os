// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros korisnik ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class korisnik {
    public static native int 파일서술자열기(int[] Datoteka_stavka_ime, int otvoren_Postavke);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int bajt_VALUE);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int izvršavanje_skladište_datoteka(int 파일서술자);
    public static native int 파일읽기(int[] ime, int[] podaci);
    public static native int 문자쓰기(int 문자);
    public static native int 파일쓰기(int[] ime, int[] podaci, int 길이);
    public static native int 쓰기(String Sadržaj_VALUE);
    public static native int 인수개수();
    public static native String 인수(int INDEX);
    public static native int 실행권한();
    public static native int otvoren_Mreža(int lokalni_port);
    public static native int poslati_podaci(int pokazivač_VALUE, int adresa, int odredište_port, int[] podaci, int 길이);
    public static native int primiti_podaci(int pokazivač_VALUE, int[] podaci, int 제한밀리초);
    public static native int Zatvori_Mreža(int pokazivač_VALUE);
    public static native int 내주소();
    public static native int 보낸주소(int pokazivač_VALUE);
    public static native int 보낸창구(int pokazivač_VALUE);
}
