// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 mašina 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class ploča {
    public static native int 표시화소읽기(int 가로, int Vertikalno_položaj);
    public static native void pisati_ekran_pel(int 가로, int Vertikalno_položaj, int 색);
    public static native int daljinsko_upravljanje(int 종류, int radnja);
    public static native void završiti_udaljeno_komanda(int stanje_VALUE);
    public static native void udaljeno_čekaj(int stanje_VALUE);
    public static native void 직렬쓰기(int VALUE);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int CPU_dozvola_nivo();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int Vertikalno_položaj, int 색);
    public static native void YIELD_CPU();
    public static native int Create_zadatak(int INDEX);
    public static native int zadatak_stanje(int INDEX);
    public static native void Zaustavi(int stanje_VALUE);
    public static native int 씨플러스시험();
    public static native int niz_korisnik_program(int INDEX);
    public static native int ček_korisnik_program();
    public static native int 인수준비(int stavka_COUNT);
    public static native int Izvrši_korisnik_fajl();
    public static native int 리눅스파일실행();
    public static native int argument_bajt(int INDEX, int Pozicija, int VALUE);
    public static native int Terminal(int radnja);
    public static native int kontrola_korisnik_program(int radnja);
    public static native void 입출력전환(int radnja);
    public static native int fajl_prijenos_usluga(int radnja);
    public static native int Mreža_stanje(int unos_VALUE, int INDEX);
    public static native int Mreža_Postavke(int radnja, int adresa, int maska_VALUE, int pristupni_uređaj_VALUE);
    public static native int 응답보내기(int adresa, int redoslijed_VALUE);
    public static native int 응답읽기(int unos_VALUE);
    public static native int upit_sistem(int unos_VALUE, int INDEX);
    public static native void 전원끄기();
}
