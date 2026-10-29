// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 Værktøjer 전용 SVC Tilslut. 기존 x86 Værktøjer 원문을 함께 빌드한다. */
public final class bruger {
    public static native int 파일서술자열기(int[] Navn, int Indstillinger);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int VÆRDI);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] Navn, int[] data);
    public static native int skrive_fil(int[] Navn, int[] data, int varighed_VÆRDI);
    public static native int Skrive(String Tekst);
    public static native int skrive_tegn_VÆRDI(int VÆRDI);
    public static native int 인수개수();
    public static native String Argumenter(int INDEKS);
    public static native int værktøj_tal();
    public static native int skærmbillede_forbindelse(int Handling, int INDEKS, int 가, int SEKUND_operand, int 다, int 라);
    public static native int skærmbillede_sms(int INDEKS, int[] Tekst, int varighed_VÆRDI);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int strøm_kontrol(int Handling, int 서술자, int VÆRDI);
    public static native int Forbind_strøm(int 서술자, int mail, int port_VÆRDI);
    public static native int åben_netværk(int port_VÆRDI);
    public static native int maile_netværk(int 서술자, int mail, int port_VÆRDI, int[] data, int varighed_VÆRDI);
    public static native int modtage_netværk(int 서술자, int[] data, int varighed_VÆRDI);
    public static native int netværk_port(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int rektangel(int 가로, int Lodret_placere, int 폭, int 높이, int 색);
}
