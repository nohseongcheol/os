// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros korisnik ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class korisnik {
    public static native int 파일서술자열기(int[] Datoteka_unos_naziv, int otvoreno_Postavke);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int bajt_VALUE);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int izvršavanje_pohrana_datoteka(int 파일서술자);
    public static native int 파일읽기(int[] Ime, int[] podaci);
    public static native int zapisivanje_znak_VALUE(int 문자);
    public static native int zapisivanje_Datoteka(int[] Ime, int[] podaci, int 길이);
    public static native int Zapisuj(String Sadržaj_VALUE);
    public static native int 인수개수();
    public static native String Argumenti(int INDEX);
    public static native int 실행권한();
    public static native int otvoreno_mreža(int lokalno_prebaciti);
    public static native int slati_podaci(int ustroj_VALUE, int adresa, int odredište_prebaciti, int[] podaci, int 길이);
    public static native int primiti_podaci(int ustroj_VALUE, int[] podaci, int 제한밀리초);
    public static native int Zatvori_mreža(int ustroj_VALUE);
    public static native int 내주소();
    public static native int 보낸주소(int ustroj_VALUE);
    public static native int 보낸창구(int ustroj_VALUE);
}
