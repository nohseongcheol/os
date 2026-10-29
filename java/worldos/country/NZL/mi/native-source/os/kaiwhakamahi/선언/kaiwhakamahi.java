// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros kaiwhakamahi ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class kaiwhakamahi {
    public static native int 파일서술자열기(int[] kōnae_tāurunga_ingoa, int tiwhikete_Ngā_Tautuhinga);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int paita_uara);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] Ingoa, int[] raraunga);
    public static native int tuhi_pūāhua_uara(int 문자);
    public static native int tuhi_kōnae(int[] Ingoa, int[] raraunga, int roa_uara);
    public static native int Tuhia(String Ihirangi_uara);
    public static native int 인수개수();
    public static native String 인수(int INDEX);
    public static native int 실행권한();
    public static native int tiwhikete_whatunga(int paetata_kawe);
    public static native int tuku_raraunga(int raweke_uara, int ADDRESS, int ūnga_kawe, int[] raraunga, int roa_uara);
    public static native int 자료받기(int raweke_uara, int[] raraunga, int 제한밀리초);
    public static native int kati_whatunga(int raweke_uara);
    public static native int 내주소();
    public static native int 보낸주소(int raweke_uara);
    public static native int 보낸창구(int raweke_uara);
}
