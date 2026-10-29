// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 počítač_5eb260fa 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class Panel {
    public static native int 표시화소읽기(int 가로, int vertikála_pozícia);
    public static native void zapísať_displej_pixel(int 가로, int vertikála_pozícia, int 색);
    public static native int tieňové_ovládanie(int 종류, int Akcia);
    public static native void ukončiť_hovor_vzdialený_príkaz(int Stav_VALUE);
    public static native void vzdialený_počkaj(int Stav_VALUE);
    public static native void 직렬쓰기(int VALUE);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int procesor_povolenie_úroveň();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int vertikála_pozícia, int 색);
    public static native void YIELD_procesor();
    public static native int Create_úloha(int INDEX);
    public static native int úloha_Stav(int INDEX);
    public static native void Zastaviť(int Stav_VALUE);
    public static native int 씨플러스시험();
    public static native int spustiť_používateľ_program(int INDEX);
    public static native int skontrolovať_používateľ_program();
    public static native int 인수준비(int položka_COUNT);
    public static native int Vykonať_používateľ_Súbor();
    public static native int 리눅스파일실행();
    public static native int argument_Byte(int INDEX, int Pozícia, int VALUE);
    public static native int Terminál(int Akcia);
    public static native int riadenie_používateľ_program(int Akcia);
    public static native void 입출력전환(int Akcia);
    public static native int prenos_súborov_služba(int Akcia);
    public static native int sieť_stav(int položka_VALUE, int INDEX);
    public static native int sieť_Nastavenia(int Akcia, int adresa, int maska_VALUE, int brána_VALUE);
    public static native int odoslať_odpoveď(int adresa, int poradie_VALUE);
    public static native int 응답읽기(int položka_VALUE);
    public static native int dotaz_systém(int položka_VALUE, int INDEX);
    public static native void 전원끄기();
}
