// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros naudotojas ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class naudotojas {
    public static native int 파일서술자열기(int[] Failas_įrašas_pavadinimas, int kurti_Parametrai);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int baitas_VALUE);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int vykdymas_failų_saugykla(int 파일서술자);
    public static native int 파일읽기(int[] Pavadinimas_2, int[] duomenys);
    public static native int rašymas_simbolis_VALUE(int 문자);
    public static native int rašymas_Failas(int[] Pavadinimas_2, int[] duomenys, int 길이);
    public static native int Rašymas(String Turinys_VALUE);
    public static native int 인수개수();
    public static native String Argumentai(int INDEX);
    public static native int 실행권한();
    public static native int kurti_tinklas(int vietinis_jungtis);
    public static native int siųsti_duomenys(int rodyklė_VALUE, int ADDRESS, int vieta_jungtis, int[] duomenys, int 길이);
    public static native int gauti_duomenys(int rodyklė_VALUE, int[] duomenys, int 제한밀리초);
    public static native int Uždaryti_tinklas(int rodyklė_VALUE);
    public static native int 내주소();
    public static native int 보낸주소(int rodyklė_VALUE);
    public static native int 보낸창구(int rodyklė_VALUE);
}
