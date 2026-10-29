// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros felhasználó ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class felhasználó {
    public static native int 파일서술자열기(int[] Fájl_bejegyzés_név, int készít_Gépház);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int bájt_ÉRTÉK);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int véglegesít_Files(int 파일서술자);
    public static native int 파일읽기(int[] Név, int[] adat);
    public static native int ír_karakter_ÉRTÉK(int 문자);
    public static native int ír_Fájl(int[] Név, int[] adat, int hossz_ÉRTÉK);
    public static native int Írás(String Tartalom_ÉRTÉK);
    public static native int 인수개수();
    public static native String Argumentumok(int INDEX);
    public static native int végrehajtás_engedély();
    public static native int készít_hálózat(int helyi_port);
    public static native int küld_adat(int leíró_ÉRTÉK, int CÍM, int cél_port, int[] adat, int hossz_ÉRTÉK);
    public static native int fogad_adat(int leíró_ÉRTÉK, int[] adat, int 제한밀리초);
    public static native int bezár_hálózat(int leíró_ÉRTÉK);
    public static native int 내주소();
    public static native int 보낸주소(int leíró_ÉRTÉK);
    public static native int 보낸창구(int leíró_ÉRTÉK);
}
