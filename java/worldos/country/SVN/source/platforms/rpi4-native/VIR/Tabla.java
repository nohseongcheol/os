// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 računalnik 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class Tabla {
    public static native int 표시화소읽기(int 가로, int Navpično_položaj);
    public static native void pisati_zaslon_slikovna_pika(int 가로, int Navpično_položaj, int 색);
    public static native int oddaljeni_nadzor(int 종류, int Dejanje);
    public static native void končati_klic_oddaljen_ukaz(int stanje_VALUE);
    public static native void oddaljen_počakaj(int stanje_VALUE);
    public static native void 직렬쓰기(int VALUE);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int CPE_pravica_raven();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int Navpično_položaj, int 색);
    public static native void YIELD_CPE();
    public static native int Ustvari_opravek(int INDEX);
    public static native int opravek_stanje(int INDEX);
    public static native void Zaustavi(int stanje_VALUE);
    public static native int 씨플러스시험();
    public static native int izvajati_uporabnik_aplikacija(int INDEX);
    public static native int preveriti_uporabnik_aplikacija();
    public static native int 인수준비(int element_COUNT);
    public static native int Izvedi_uporabnik_Datoteka();
    public static native int 리눅스파일실행();
    public static native int argument_bajt(int INDEX, int Položaj, int VALUE);
    public static native int Terminal(int Dejanje);
    public static native int nadzor_uporabnik_aplikacija(int Dejanje);
    public static native void 입출력전환(int Dejanje);
    public static native int prenos_datotek_storitev(int Dejanje);
    public static native int mreža_stanje(int vnos_VALUE, int INDEX);
    public static native int mreža_Nastavitve(int Dejanje, int naslov, int maska_VALUE, int prehod_VALUE);
    public static native int poslati_odziv(int naslov, int naročilo_VALUE);
    public static native int 응답읽기(int vnos_VALUE);
    public static native int poizvedba_sistem(int vnos_VALUE, int INDEX);
    public static native void 전원끄기();
}
