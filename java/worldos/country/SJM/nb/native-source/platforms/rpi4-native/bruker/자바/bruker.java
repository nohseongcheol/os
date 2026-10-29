// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 Verktøy 전용 SVC Koble_til. 기존 x86 Verktøy 원문을 함께 빌드한다. */
public final class bruker {
    public static native int 파일서술자열기(int[] Navn, int Innstillinger);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int VERDI);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] Navn, int[] data);
    public static native int skrive_Fil(int[] Navn, int[] data, int lengde_VERDI);
    public static native int Skriv(String Tekst);
    public static native int skrive_tegn_VERDI(int VERDI);
    public static native int 인수개수();
    public static native String Argumenter(int INDEKS);
    public static native int verktøy_nummer();
    public static native int skjermbilde_kontakt(int Handling, int INDEKS, int 가, int SEKUND_operand, int 다, int 라);
    public static native int skjermbilde_SMS(int INDEKS, int[] Tekst, int lengde_VERDI);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int strøm_kontroll(int Handling, int 서술자, int VERDI);
    public static native int KOBLE_TIL_strøm(int 서술자, int e_post, int port_VERDI);
    public static native int åpen_nettverk(int port_VERDI);
    public static native int sende_nettverk(int 서술자, int e_post, int port_VERDI, int[] data, int lengde_VERDI);
    public static native int motta_nettverk(int 서술자, int[] data, int lengde_VERDI);
    public static native int nettverk_port(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int rektangel(int 가로, int vertikal_plassere, int 폭, int 높이, int 색);
}
