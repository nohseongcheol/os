// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 Orodja 전용 SVC Poveži. 기존 x86 Orodja 원문을 함께 빌드한다. */
public final class uporabnik {
    public static native int 파일서술자열기(int[] Ime, int Nastavitve);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int VALUE);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] Ime, int[] podatki);
    public static native int pisati_Datoteka(int[] Ime, int[] podatki, int 길이);
    public static native int Pisanje(String Besedilo);
    public static native int pisati_znak_VALUE(int VALUE);
    public static native int 인수개수();
    public static native String Argumenti(int INDEX);
    public static native int 도구번호();
    public static native int 화면연결(int Dejanje, int INDEX, int 가, int SECOND_operand, int 다, int 라);
    public static native int 화면글(int INDEX, int[] Besedilo, int 길이);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int tok_nadzor(int Dejanje, int 서술자, int VALUE);
    public static native int POVEŽI_tok(int 서술자, int naslov, int vrata_VALUE);
    public static native int odprto_mreža(int vrata_VALUE);
    public static native int poslati_mreža(int 서술자, int naslov, int vrata_VALUE, int[] podatki, int 길이);
    public static native int sprejeti_sprejemati_prejeti_prejemati_mreža(int 서술자, int[] podatki, int 길이);
    public static native int mreža_vrata(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int pravokotnik(int 가로, int Navpično_položaj, int 폭, int višina_VALUE, int 색);
}
