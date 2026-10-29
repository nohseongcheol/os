// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 verktyg 전용 SVC Anslut. 기존 x86 verktyg 원문을 함께 빌드한다. */
public final class användarutrymme {
    public static native int 파일서술자열기(int[] Namn, int Inställningar);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int värde);
    public static native int 파일서술자닫기(int 서술자);
    public static native int läsa_fil(int[] Namn, int[] data);
    public static native int skriva_fil(int[] Namn, int[] data, int längd_värde);
    public static native int Skriv(String text);
    public static native int skriva_tecken_värde(int värde);
    public static native int 인수개수();
    public static native String argument(int INDEX);
    public static native int verktyg_nummer();
    public static native int skärmbild_kontakt(int Åtgärd, int INDEX, int 가, int SEKUND_operand, int 다, int 라);
    public static native int skärmbild_SMS(int INDEX, int[] text, int längd_värde);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int flöde_kontroll(int Åtgärd, int 서술자, int värde);
    public static native int ANSLUT_flöde(int 서술자, int Adress, int port_värde);
    public static native int skapa_nätverk(int port_värde);
    public static native int skicka_nätverk(int 서술자, int Adress, int port_värde, int[] data, int längd_värde);
    public static native int få_nätverk(int 서술자, int[] data, int längd_värde);
    public static native int nätverk_port(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int rektangel(int 가로, int bransch_placera, int 폭, int 높이, int 색);
}
