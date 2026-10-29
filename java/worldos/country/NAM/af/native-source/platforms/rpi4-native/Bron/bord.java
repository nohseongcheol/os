// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 masjien 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class bord {
    public static native int 표시화소읽기(int 가로, int Vertikaal_plaas);
    public static native void skryf_wys_pieksel(int 가로, int Vertikaal_plaas, int 색);
    public static native int skaduwing(int 종류, int Aksie);
    public static native void beëindig_afstands_bevel(int stand_VALUE);
    public static native void afstands_wag(int stand_VALUE);
    public static native void 직렬쓰기(int VALUE);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int SVE_toestemming_vlak();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int Vertikaal_plaas, int 색);
    public static native void YIELD_SVE();
    public static native int Skep_taak(int INDEX);
    public static native int taak_stand(int INDEX);
    public static native void Stop(int stand_VALUE);
    public static native int 씨플러스시험();
    public static native int ry_gebruiker_program(int INDEX);
    public static native int tjek_gebruiker_program();
    public static native int 인수준비(int item_COUNT);
    public static native int uitvoer_gebruiker_lêer();
    public static native int 리눅스파일실행();
    public static native int argument_greep(int INDEX, int Posisie, int VALUE);
    public static native int Terminaal(int Aksie);
    public static native int kontrole_gebruiker_program(int Aksie);
    public static native void 입출력전환(int Aksie);
    public static native int lêer_oordra_diens(int Aksie);
    public static native int Netwerk_stand(int inskrywing_VALUE, int INDEX);
    public static native int Netwerk_Instellings(int Aksie, int adres, int masker_VALUE, int deurgang_VALUE);
    public static native int 응답보내기(int adres, int volgorde_VALUE);
    public static native int 응답읽기(int inskrywing_VALUE);
    public static native int navraag_stelsel(int inskrywing_VALUE, int INDEX);
    public static native void 전원끄기();
}
