// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 Alati 전용 SVC Spoji_se. 기존 x86 Alati 원문을 함께 빌드한다. */
public final class korisnik {
    public static native int 파일서술자열기(int[] Ime, int Postavke);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int VALUE);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] Ime, int[] podaci);
    public static native int zapisivanje_Datoteka(int[] Ime, int[] podaci, int 길이);
    public static native int Zapisuj(String Tekst);
    public static native int zapisivanje_znak_VALUE(int VALUE);
    public static native int 인수개수();
    public static native String Argumenti(int INDEX);
    public static native int 도구번호();
    public static native int 화면연결(int Aktivnost, int INDEX, int 가, int SECOND_operand, int 다, int 라);
    public static native int 화면글(int INDEX, int[] Tekst, int 길이);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int tok_kontrola(int Aktivnost, int 서술자, int VALUE);
    public static native int CONNECT_tok(int 서술자, int adresa, int prebaciti_VALUE);
    public static native int otvoreno_mreža(int prebaciti_VALUE);
    public static native int slati_mreža(int 서술자, int adresa, int prebaciti_VALUE, int[] podaci, int 길이);
    public static native int primiti_mreža(int 서술자, int[] podaci, int 길이);
    public static native int mreža_prebaciti(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int pravokutnik(int 가로, int Okomito_položaj, int 폭, int 높이, int 색);
}
