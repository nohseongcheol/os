// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros mošomiši ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class mošomiši {
    public static native int 파일서술자열기(int[] faele_go_tsenya_tshedimošo_leina, int bula_Dipeakanyo);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int paete_boleng);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] Leina, int[] data);
    public static native int ngwala_tlhaka_boleng(int 문자);
    public static native int ngwala_faele(int[] Leina, int[] data, int botelele_boleng);
    public static native int Ngwala(String Diteng_boleng);
    public static native int 인수개수();
    public static native String 인수(int lokela);
    public static native int 실행권한();
    public static native int bula_Netweke(int kgauswi_phote);
    public static native int Romela_data(int tshwaro_boleng, int atrese, int boyo_phote, int[] data, int botelele_boleng);
    public static native int 자료받기(int tshwaro_boleng, int[] data, int 제한밀리초);
    public static native int tswalela_Netweke(int tshwaro_boleng);
    public static native int 내주소();
    public static native int 보낸주소(int tshwaro_boleng);
    public static native int 보낸창구(int tshwaro_boleng);
}
