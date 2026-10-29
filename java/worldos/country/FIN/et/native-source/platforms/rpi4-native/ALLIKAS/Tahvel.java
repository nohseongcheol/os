// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 arvuti 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class Tahvel {
    public static native int 표시화소읽기(int 가로, int vertikaal_ametikoht);
    public static native void kirjutamine_ekraan_piksel(int 가로, int vertikaal_ametikoht, int 색);
    public static native int varikasutus(int 종류, int Nimi);
    public static native void lõpeta_kõne_kauge_käsk(int Olek_VALUE);
    public static native void kauge_Oota(int Olek_VALUE);
    public static native void 직렬쓰기(int VALUE);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int CPU_luba_tase();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int vertikaal_ametikoht, int 색);
    public static native void YIELD_CPU();
    public static native int avama_tööüksus(int INDEX);
    public static native int tööüksus_Olek(int INDEX);
    public static native void Peata(int Olek_VALUE);
    public static native int 씨플러스시험();
    public static native int sari_kasutaja_programm(int INDEX);
    public static native int tšekk_kasutaja_programm();
    public static native int 인수준비(int kaup_COUNT);
    public static native int Täida_kasutaja_Fail();
    public static native int 리눅스파일실행();
    public static native int argument_bait(int INDEX, int Asukoht, int VALUE);
    public static native int terminal(int Nimi);
    public static native int meede_kasutaja_programm(int Nimi);
    public static native void 입출력전환(int Nimi);
    public static native int failiedastus_teenus(int Nimi);
    public static native int võrk_olek(int kirje_VALUE, int INDEX);
    public static native int võrk_Sätted(int Nimi, int ADDRESS, int mask_VALUE, int lüüs_VALUE);
    public static native int saatma_vastus(int ADDRESS, int tellimus_VALUE);
    public static native int 응답읽기(int kirje_VALUE);
    public static native int päring_süsteem(int kirje_VALUE, int INDEX);
    public static native void 전원끄기();
}
