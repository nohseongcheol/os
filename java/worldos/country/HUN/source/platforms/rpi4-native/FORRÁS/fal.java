// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 gép határ_ÉRTÉK. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class fal {
    public static native int 표시화소읽기(int 가로, int szektor_pozíció);
    public static native void ír_kijelző_képpont(int 가로, int szektor_pozíció, int 색);
    public static native int távkezelés(int Altípus_ÉRTÉK, int Művelet);
    public static native void megszüntet_távoli_parancs(int Állapot_ÉRTÉK);
    public static native void távoli_várj(int Állapot_ÉRTÉK);
    public static native void 직렬쓰기(int ÉRTÉK);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int CPU_jog_szint();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int szektor_pozíció, int 색);
    public static native void HOZAM_CPU();
    public static native int készít_teendő(int INDEX);
    public static native int teendő_Állapot(int INDEX);
    public static native void Leállítás(int Állapot_ÉRTÉK);
    public static native int 씨플러스시험();
    public static native int futtat_felhasználó_app(int INDEX);
    public static native int csekk_felhasználó_app();
    public static native int 인수준비(int cikk_DARAB);
    public static native int végrehajt_felhasználó_Fájl();
    public static native int 리눅스파일실행();
    public static native int argumentum_bájt(int INDEX, int Pozíció, int ÉRTÉK);
    public static native int Terminál(int Művelet);
    public static native int vezérlő_felhasználó_app(int Művelet);
    public static native void 입출력전환(int Művelet);
    public static native int fájlátvitel_szolgáltatás(int Művelet);
    public static native int hálózat_állapot(int bejegyzés_ÉRTÉK, int INDEX);
    public static native int hálózat_Gépház(int Művelet, int CÍM, int maszk_ÉRTÉK, int átjáró_ÉRTÉK);
    public static native int küld_válasz(int CÍM, int rendel_ÉRTÉK);
    public static native int 응답읽기(int bejegyzés_ÉRTÉK);
    public static native int lekérdez_Rendszer(int bejegyzés_ÉRTÉK, int INDEX);
    public static native void 전원끄기();
}
