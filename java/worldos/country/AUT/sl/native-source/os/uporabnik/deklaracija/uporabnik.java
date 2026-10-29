// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros uporabnik ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class uporabnik {
    public static native int 파일서술자열기(int[] Datoteka_vnos_ime, int odprto_Nastavitve);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int bajt_VALUE);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int potrjevanje_datotečna_shramba(int 파일서술자);
    public static native int 파일읽기(int[] Ime, int[] podatki);
    public static native int pisati_znak_VALUE(int 문자);
    public static native int pisati_Datoteka(int[] Ime, int[] podatki, int 길이);
    public static native int Pisanje(String vsebina_VALUE);
    public static native int 인수개수();
    public static native String Argumenti(int INDEX);
    public static native int 실행권한();
    public static native int odprto_mreža(int lokalen_krajeven_vrata);
    public static native int poslati_podatki(int ročica_VALUE, int naslov, int cilj_vrata, int[] podatki, int 길이);
    public static native int sprejeti_sprejemati_prejeti_prejemati_podatki(int ročica_VALUE, int[] podatki, int 제한밀리초);
    public static native int Zapri_mreža(int ročica_VALUE);
    public static native int 내주소();
    public static native int 보낸주소(int ročica_VALUE);
    public static native int 보낸창구(int ročica_VALUE);
}
