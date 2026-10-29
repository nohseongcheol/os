// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 računar 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class Tabla {
    public static native int 표시화소읽기(int 가로, int vertikala_pozicija);
    public static native void 표시화소쓰기(int 가로, int vertikala_pozicija, int 색);
    public static native int daljinska_kontrola(int 종류, int radnja);
    public static native void završiti_razgovor_udaljen_komanda(int Status_VALUE);
    public static native void udaljen_čekaj(int Status_VALUE);
    public static native void 직렬쓰기(int VALUE);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int CPU_dozvola_nivo();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int vertikala_pozicija, int 색);
    public static native void YIELD_CPU();
    public static native int Create_obaveza(int INDEX);
    public static native int obaveza_Status(int INDEX);
    public static native void Stani(int Status_VALUE);
    public static native int 씨플러스시험();
    public static native int koristiti_korisnik_program(int INDEX);
    public static native int proveriti_korisnik_program();
    public static native int 인수준비(int stavka_COUNT);
    public static native int Izvrši_korisnik_Datoteka();
    public static native int 리눅스파일실행();
    public static native int argument_bajt(int INDEX, int pozicija, int VALUE);
    public static native int Terminal(int radnja);
    public static native int kontrola_korisnik_program(int radnja);
    public static native void 입출력전환(int radnja);
    public static native int prenos_datoteka_usluga(int radnja);
    public static native int Mreža_status(int stavka_VALUE, int INDEX);
    public static native int Mreža_Postavke(int radnja, int adresa, int maska_VALUE, int mrežni_prolaz_VALUE);
    public static native int poslati_odgovor(int adresa, int poručiti_VALUE);
    public static native int 응답읽기(int stavka_VALUE);
    public static native int upit_sistem(int stavka_VALUE, int INDEX);
    public static native void 전원끄기();
}
