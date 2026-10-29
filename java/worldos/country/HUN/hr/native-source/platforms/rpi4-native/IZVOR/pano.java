// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 stroj 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class pano {
    public static native int 표시화소읽기(int 가로, int Okomito_položaj);
    public static native void zapisivanje_zaslon_slikovni_element(int 가로, int Okomito_položaj, int 색);
    public static native int paralelna_sesija(int 종류, int Aktivnost);
    public static native void završiti_razgovor_udaljeno_naredba(int Stanje_VALUE);
    public static native void udaljeno_čekaj(int Stanje_VALUE);
    public static native void 직렬쓰기(int VALUE);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int CPU_dozvola_razina();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int Okomito_položaj, int 색);
    public static native void YIELD_CPU();
    public static native int Create_obaveza(int INDEX);
    public static native int obaveza_Stanje(int INDEX);
    public static native void Zaustavi(int Stanje_VALUE);
    public static native int 씨플러스시험();
    public static native int izvršiti_korisnik_program(int INDEX);
    public static native int 사용자검사();
    public static native int 인수준비(int artikl_COUNT);
    public static native int Izvrši_korisnik_Datoteka();
    public static native int 리눅스파일실행();
    public static native int argument_bajt(int INDEX, int Položaj, int VALUE);
    public static native int Terminal(int Aktivnost);
    public static native int kontrola_korisnik_program(int Aktivnost);
    public static native void 입출력전환(int Aktivnost);
    public static native int prijenos_datoteka_servis(int Aktivnost);
    public static native int mreža_stanje(int unos_VALUE, int INDEX);
    public static native int mreža_Postavke(int Aktivnost, int adresa, int maska_VALUE, int pristupnik_VALUE);
    public static native int slati_odgovor(int adresa, int narudžba_VALUE);
    public static native int 응답읽기(int unos_VALUE);
    public static native int upit_sustav(int unos_VALUE, int INDEX);
    public static native void 전원끄기();
}
