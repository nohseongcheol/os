// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros Mai_anfani_da_kwamfuta ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class Mai_anfani_da_kwamfuta {
    public static native int 파일서술자열기(int[] Fayil_Mashigar_bayanai_Suna, int buɗe_Saituna);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int bayit_Daraja);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] Suna, int[] Tarin_bayani);
    public static native int Rubuta_Harafi_Daraja(int 문자);
    public static native int Rubuta_Fayil(int[] Suna, int[] Tarin_bayani, int Tsawo_Daraja);
    public static native int Yi_Rubutu(String kunshiya_Daraja);
    public static native int 인수개수();
    public static native String 인수(int Indes);
    public static native int 실행권한();
    public static native int buɗe_Hanyar_sadarwa(int na_gida_fot);
    public static native int Aika_Tarin_bayani(int Mariki_Daraja, int imel, int Zangon_ƙarshe_fot, int[] Tarin_bayani, int Tsawo_Daraja);
    public static native int 자료받기(int Mariki_Daraja, int[] Tarin_bayani, int 제한밀리초);
    public static native int Rufe_Hanyar_sadarwa(int Mariki_Daraja);
    public static native int 내주소();
    public static native int 보낸주소(int Mariki_Daraja);
    public static native int 보낸창구(int Mariki_Daraja);
}
