// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 počítač mez_HODNOTA. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class Panel {
    public static native int 표시화소읽기(int 가로, int Svislá_pozice);
    public static native void zápis_displej_pixel(int 가로, int Svislá_pozice, int 색);
    public static native int stínový_provoz(int Druh_HODNOTA, int Akce);
    public static native void konec_vzdálený_příkaz(int Stav_HODNOTA);
    public static native void vzdálený_počkej(int Stav_HODNOTA);
    public static native void 직렬쓰기(int HODNOTA);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int CPU_oprávnění_úroveň();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int Svislá_pozice, int 색);
    public static native void YIELD_CPU();
    public static native int Create_úkol(int INDEX);
    public static native int úkol_Stav(int INDEX);
    public static native void Zastavit(int Stav_HODNOTA);
    public static native int 씨플러스시험();
    public static native int spustit_uživatel_program(int INDEX);
    public static native int šek_uživatel_program();
    public static native int 인수준비(int zboží_POČET);
    public static native int Provést_uživatel_Soubor();
    public static native int 리눅스파일실행();
    public static native int argument_bajt(int INDEX, int pozice, int HODNOTA);
    public static native int interpret_příkazů(int Akce);
    public static native int řízení_uživatel_program(int Akce);
    public static native void 입출력전환(int Akce);
    public static native int přenos_souborů_servis(int Akce);
    public static native int síť_stav(int položka_HODNOTA, int INDEX);
    public static native int síť_Nastavení(int Akce, int Adresa, int maska_HODNOTA, int brána_HODNOTA);
    public static native int poslat_odpověď(int Adresa, int pořadí_HODNOTA);
    public static native int 응답읽기(int položka_HODNOTA);
    public static native int dotaz_Systém(int položka_HODNOTA, int INDEX);
    public static native void 전원끄기();
}
