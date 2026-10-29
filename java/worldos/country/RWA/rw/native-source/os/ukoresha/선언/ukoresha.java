// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros ukoresha ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class ukoresha {
    public static native int 파일서술자열기(int[] dosiye_icyinjizwa_izina, int kurema_Amagenamiterere);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int bayiti_agaciro);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] Izina, int[] amakurushingiro);
    public static native int kwandika_inyuguti_agaciro(int 문자);
    public static native int kwandika_dosiye(int[] Izina, int[] amakurushingiro, int uburebure_agaciro);
    public static native int kwandika(String Ibirimo_agaciro);
    public static native int 인수개수();
    public static native String 인수(int umugerekashakiro);
    public static native int 실행권한();
    public static native int kurema_Urusobemiyoboro(int mu_gace_poti);
    public static native int kohereza_amakurushingiro(int umukondo_agaciro, int aderesi, int aho_ijya_poti, int[] amakurushingiro, int uburebure_agaciro);
    public static native int 자료받기(int umukondo_agaciro, int[] amakurushingiro, int 제한밀리초);
    public static native int gufunga_Urusobemiyoboro(int umukondo_agaciro);
    public static native int 내주소();
    public static native int 보낸주소(int umukondo_agaciro);
    public static native int 보낸창구(int umukondo_agaciro);
}
