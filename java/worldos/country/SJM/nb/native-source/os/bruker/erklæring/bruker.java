// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros bruker ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class bruker {
    public static native int 파일서술자열기(int[] Fil_oppføring_navn, int åpen_Innstillinger);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int byte_VERDI);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] Navn, int[] data);
    public static native int skrive_tegn_VERDI(int 문자);
    public static native int skrive_Fil(int[] Navn, int[] data, int lengde_VERDI);
    public static native int Skriv(String Innhold_VERDI);
    public static native int 인수개수();
    public static native String Argumenter(int INDEKS);
    public static native int kjøring_tillatelse();
    public static native int åpen_nettverk(int lokal_port);
    public static native int sende_data(int håndtak_VERDI, int e_post, int mål_port, int[] data, int lengde_VERDI);
    public static native int motta_data(int håndtak_VERDI, int[] data, int 제한밀리초);
    public static native int Lukk_nettverk(int håndtak_VERDI);
    public static native int 내주소();
    public static native int 보낸주소(int håndtak_VERDI);
    public static native int 보낸창구(int håndtak_VERDI);
}
