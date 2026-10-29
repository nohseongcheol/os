// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros ka_yataayakalü ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class ka_yataayakalü {
    public static native int 파일서술자열기(int[] 파일이름, int 열기설정);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int waai_ajutuu);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] 이름, int[] atijaaya);
    public static native int ashajaa_jeerü_ajutuu(int 문자);
    public static native int ashajaa_anaajaalaa(int[] 이름, int[] atijaaya, int akaliaa_ajutuu);
    public static native int ashajaa(String alu_ujatüü_ajutuu);
    public static native int 인수개수();
    public static native String 인수(int ee_iyatialujuna);
    public static native int 실행권한();
    public static native int 통신열기(int 지역창구);
    public static native int ajütaa_atijaaya(int aapaaya_ajutuu, int ejepüsee, int jalamüinjatü_outtülee, int[] atijaaya, int akaliaa_ajutuu);
    public static native int 자료받기(int aapaaya_ajutuu, int[] atijaaya, int 제한밀리초);
    public static native int asürülaa_kusu(int aapaaya_ajutuu);
    public static native int 내주소();
    public static native int 보낸주소(int aapaaya_ajutuu);
    public static native int 보낸창구(int aapaaya_ajutuu);
}
