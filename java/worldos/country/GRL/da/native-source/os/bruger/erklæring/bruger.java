// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros bruger ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class bruger {
    public static native int 파일서술자열기(int[] fil_post_navn, int åben_Indstillinger);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int byte_VÆRDI);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int udføre_Files(int 파일서술자);
    public static native int 파일읽기(int[] Navn, int[] data);
    public static native int skrive_tegn_VÆRDI(int 문자);
    public static native int skrive_fil(int[] Navn, int[] data, int varighed_VÆRDI);
    public static native int Skrive(String Indhold_VÆRDI);
    public static native int 인수개수();
    public static native String Argumenter(int INDEKS);
    public static native int udførelse_rettighed();
    public static native int åben_netværk(int lokal_port);
    public static native int maile_data(int handle_VÆRDI, int mail, int destination_port, int[] data, int varighed_VÆRDI);
    public static native int modtage_data(int handle_VÆRDI, int[] data, int 제한밀리초);
    public static native int Luk_netværk(int handle_VÆRDI);
    public static native int 내주소();
    public static native int 보낸주소(int handle_VÆRDI);
    public static native int 보낸창구(int handle_VÆRDI);
}
