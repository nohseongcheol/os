// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 gailu 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class arbel {
    public static native int 표시화소읽기(int 가로, int Bertikala_kargu);
    public static native void idatzi_pantaila_pixel(int 가로, int Bertikala_kargu, int 색);
    public static native int aldi_bereko_saio(int 종류, int Ekintza);
    public static native void amaitu_urruneko_komando(int Egoera_balio);
    public static native void urruneko_itxaron(int Egoera_balio);
    public static native void 직렬쓰기(int balio);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int PUZ_baimen_maila();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int Bertikala_kargu, int 색);
    public static native void YIELD_PUZ();
    public static native int sortu_ataza(int INDIZE);
    public static native int ataza_Egoera(int INDIZE);
    public static native void Gelditu(int Egoera_balio);
    public static native int 씨플러스시험();
    public static native int exekutatu_erabiltzaile_aplik(int INDIZE);
    public static native int txeke_erabiltzaile_aplik();
    public static native int 인수준비(int elementu_ZENBATU);
    public static native int exekutatu_erabiltzaile_fitxategi();
    public static native int 리눅스파일실행();
    public static native int arg_byte(int INDIZE, int Posizioa, int balio);
    public static native int Terminala(int Ekintza);
    public static native int kontrol_erabiltzaile_aplik(int Ekintza);
    public static native void 입출력전환(int Ekintza);
    public static native int fitxategi_transferitu_zerbitzu(int Ekintza);
    public static native int sare_egoera(int sarrera_balio, int INDIZE);
    public static native int sare_Ezarpenak(int Ekintza, int helbide, int maskara_balio, int atebide_balio);
    public static native int bidali_erantzun(int helbide, int ordena_balio);
    public static native int 응답읽기(int sarrera_balio);
    public static native int kontsulta_sistema(int sarrera_balio, int INDIZE);
    public static native void 전원끄기();
}
