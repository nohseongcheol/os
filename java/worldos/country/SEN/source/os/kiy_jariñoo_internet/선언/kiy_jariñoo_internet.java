// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros kiy_jariñoo_internet ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class kiy_jariñoo_internet {
    public static native int 파일서술자열기(int[] bara_denc_dugal_xabaar_tur, int sos_Jekkal_yi);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int okte_xëyma);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] tur_253d1510, int[] mbir);
    public static native int biir_Araf_xëyma(int 문자);
    public static native int biir_bara_denc(int[] tur_253d1510, int[] mbir, int diir_xëyma);
    public static native int biir(String Këmb_xëyma);
    public static native int 인수개수();
    public static native String 인수(int àlluwa_tur);
    public static native int 실행권한();
    public static native int sos_mbaal(int dënnd_jël);
    public static native int Yónnee_mbir(int yombal_xëyma, int dëkkuwaay, int jëmmukaay_jël, int[] mbir, int diir_xëyma);
    public static native int 자료받기(int yombal_xëyma, int[] mbir, int 제한밀리초);
    public static native int Tej_mbaal(int yombal_xëyma);
    public static native int 내주소();
    public static native int 보낸주소(int yombal_xëyma);
    public static native int 보낸창구(int yombal_xëyma);
}
