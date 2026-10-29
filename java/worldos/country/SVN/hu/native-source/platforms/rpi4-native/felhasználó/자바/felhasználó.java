// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 Eszközök 전용 SVC Kapcsolódás. 기존 x86 Eszközök 원문을 함께 빌드한다. */
public final class felhasználó {
    public static native int 파일서술자열기(int[] Név, int Beállítások);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int ÉRTÉK);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] Név, int[] adat);
    public static native int ír_Fájl(int[] Név, int[] adat, int hossz_ÉRTÉK);
    public static native int Írás(String Szöveg);
    public static native int ír_karakter_ÉRTÉK(int ÉRTÉK);
    public static native int 인수개수();
    public static native String Argumentumok(int INDEX);
    public static native int eszköz_szám();
    public static native int 화면연결(int Művelet, int INDEX, int 가, int MPERC_operandus, int 다, int 라);
    public static native int 화면글(int INDEX, int[] Szöveg, int hossz_ÉRTÉK);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int Stream_vezérlő(int Művelet, int 서술자, int ÉRTÉK);
    public static native int KAPCSOLAT_Stream(int 서술자, int CÍM, int port_ÉRTÉK);
    public static native int készít_hálózat(int port_ÉRTÉK);
    public static native int küld_hálózat(int 서술자, int CÍM, int port_ÉRTÉK, int[] adat, int hossz_ÉRTÉK);
    public static native int fogad_hálózat(int 서술자, int[] adat, int hossz_ÉRTÉK);
    public static native int hálózat_port(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int téglalap(int 가로, int szektor_pozíció, int 폭, int 높이, int 색);
}
