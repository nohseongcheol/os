// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros lietotājs ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class lietotājs {
    public static native int 파일서술자열기(int[] Fails_ievade_nosaukums, int atvērt_Iestatījumi);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int byte_VALUE);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int izpilde_failu_krātuve(int 파일서술자);
    public static native int 파일읽기(int[] Nosaukums, int[] dati);
    public static native int rakstīšana_rakstzīme_VALUE(int 문자);
    public static native int rakstīšana_Fails(int[] Nosaukums, int[] dati, int 길이);
    public static native int Rakstīt(String Saturs_VALUE);
    public static native int 인수개수();
    public static native String Parametri(int INDEX);
    public static native int 실행권한();
    public static native int atvērt_tīkls(int vietējs_ports);
    public static native int sūtīt_dati(int turis_VALUE, int adrese, int mērķis_ports, int[] dati, int 길이);
    public static native int saņemt_dati(int turis_VALUE, int[] dati, int 제한밀리초);
    public static native int Aizvērt_tīkls(int turis_VALUE);
    public static native int 내주소();
    public static native int 보낸주소(int turis_VALUE);
    public static native int 보낸창구(int turis_VALUE);
}
