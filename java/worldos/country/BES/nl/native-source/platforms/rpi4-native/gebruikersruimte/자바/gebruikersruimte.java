// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 hulpmiddelen 전용 SVC Verbinden. 기존 x86 hulpmiddelen 원문을 함께 빌드한다. */
public final class gebruikersruimte {
    public static native int 파일서술자열기(int[] Naam, int Instellingen);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int WAARDE);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] Naam, int[] gegevens);
    public static native int schrijven_Bestand(int[] Naam, int[] gegevens, int tijdsduur_WAARDE);
    public static native int Schrijven(String tekst);
    public static native int schrijven_teken_WAARDE(int WAARDE);
    public static native int 인수개수();
    public static native String argumenten(int INDEX);
    public static native int hulpmiddel_nummer();
    public static native int scherm_verbinding(int Actie, int INDEX, int 가, int SECONDE_operand, int 다, int 라);
    public static native int scherm_sms(int INDEX, int[] tekst, int tijdsduur_WAARDE);
    public static native int 화면너비();
    public static native int scherm_hoogte();
    public static native int Stream_controle(int Actie, int 서술자, int WAARDE);
    public static native int VERBINDEN_Stream(int 서술자, int ADRES, int poort_WAARDE);
    public static native int open_net(int poort_WAARDE);
    public static native int e_mailen_net(int 서술자, int ADRES, int poort_WAARDE, int[] gegevens, int tijdsduur_WAARDE);
    public static native int ontvangen_net(int 서술자, int[] gegevens, int tijdsduur_WAARDE);
    public static native int net_poort(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int rechthoek(int 가로, int Verticaal_functie, int 폭, int hoogte_WAARDE, int 색);
}
