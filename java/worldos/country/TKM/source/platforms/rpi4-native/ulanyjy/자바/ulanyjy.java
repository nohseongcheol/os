// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 Gurallar 전용 SVC Birikme. 기존 x86 Gurallar 원문을 함께 빌드한다. */
public final class ulanyjy {
    public static native int 파일서술자열기(int[] Ad, int Düzümler);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int baha);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] Ad, int[] maglumat);
    public static native int ýaz_faýl(int[] Ad, int[] maglumat, int dowamlylyk_baha);
    public static native int Ýaz(String Metin);
    public static native int ýaz_nyşan_baha(int baha);
    public static native int 인수개수();
    public static native String 인수(int indeks);
    public static native int 도구번호();
    public static native int 화면연결(int iş, int indeks, int 가, int 나, int 다, int 라);
    public static native int 화면글(int indeks, int[] Metin, int dowamlylyk_baha);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int Stream_dolandyryş(int iş, int 서술자, int baha);
    public static native int Birikme_Stream(int 서술자, int salgy, int port_baha);
    public static native int aç_Tor(int port_baha);
    public static native int iber_Tor(int 서술자, int salgy, int port_baha, int[] maglumat, int dowamlylyk_baha);
    public static native int 통신받기(int 서술자, int[] maglumat, int dowamlylyk_baha);
    public static native int Tor_port(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int 세로, int 폭, int 높이, int 색);
}
