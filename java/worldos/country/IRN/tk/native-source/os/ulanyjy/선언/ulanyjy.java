// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros ulanyjy ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class ulanyjy {
    public static native int 파일서술자열기(int[] faýl_girizmeklik_at, int aç_Sazlamalar);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int baýt_baha);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] Ad, int[] maglumat);
    public static native int ýaz_nyşan_baha(int 문자);
    public static native int ýaz_faýl(int[] Ad, int[] maglumat, int dowamlylyk_baha);
    public static native int Ýaz(String Mazmun_baha);
    public static native int 인수개수();
    public static native String 인수(int indeks);
    public static native int 실행권한();
    public static native int aç_Tor(int ýerli_port);
    public static native int iber_maglumat(int ryçag_baha, int salgy, int barylmaly_ýer_port, int[] maglumat, int dowamlylyk_baha);
    public static native int 자료받기(int ryçag_baha, int[] maglumat, int 제한밀리초);
    public static native int ýap_Tor(int ryçag_baha);
    public static native int 내주소();
    public static native int 보낸주소(int ryçag_baha);
    public static native int 보낸창구(int ryçag_baha);
}
