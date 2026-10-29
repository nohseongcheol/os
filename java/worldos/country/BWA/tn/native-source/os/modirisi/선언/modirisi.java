// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros modirisi ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class modirisi {
    public static native int 파일서술자열기(int[] faele_tsenyo_leina, int bula_Diseting);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int baete_Boleng);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] leina, int[] tshedimosetso);
    public static native int kwala_Letshwao_Boleng(int 문자);
    public static native int kwala_faele(int[] leina, int[] tshedimosetso, int boleele_Boleng);
    public static native int kwala(String Diteng_Boleng);
    public static native int 인수개수();
    public static native String 인수(int tshupane);
    public static native int 실행권한();
    public static native int bula_Neteweke(int e_e_gaufi_gorogisetsa);
    public static native int romela_tshedimosetso(int mokgwakamogelo_Boleng, int aterese, int bogorogelo_gorogisetsa, int[] tshedimosetso, int boleele_Boleng);
    public static native int 자료받기(int mokgwakamogelo_Boleng, int[] tshedimosetso, int 제한밀리초);
    public static native int tswala_Neteweke(int mokgwakamogelo_Boleng);
    public static native int 내주소();
    public static native int 보낸주소(int mokgwakamogelo_Boleng);
    public static native int 보낸창구(int mokgwakamogelo_Boleng);
}
