// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros gebruikersruimte ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class gebruikersruimte {
    public static native int 파일서술자열기(int[] Bestand_invoer_naam, int open_Instellingen);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int byte_WAARDE);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int doorvoeren_Files(int 파일서술자);
    public static native int 파일읽기(int[] Naam, int[] gegevens);
    public static native int schrijven_teken_WAARDE(int 문자);
    public static native int schrijven_Bestand(int[] Naam, int[] gegevens, int tijdsduur_WAARDE);
    public static native int Schrijven(String Inhoud_WAARDE);
    public static native int 인수개수();
    public static native String argumenten(int INDEX);
    public static native int uitvoerbewerking_machtiging();
    public static native int open_net(int lokaal_poort);
    public static native int e_mailen_gegevens(int greep_WAARDE, int ADRES, int doel_poort, int[] gegevens, int tijdsduur_WAARDE);
    public static native int ontvangen_gegevens(int greep_WAARDE, int[] gegevens, int 제한밀리초);
    public static native int Sluiten_net(int greep_WAARDE);
    public static native int 내주소();
    public static native int 보낸주소(int greep_WAARDE);
    public static native int 보낸창구(int greep_WAARDE);
}
