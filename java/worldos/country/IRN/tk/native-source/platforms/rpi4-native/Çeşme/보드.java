// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 kompýuter 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class 보드 {
    public static native int 표시화소읽기(int 가로, int 세로);
    public static native void ýaz_ekran_pel(int 가로, int 세로, int 색);
    public static native int kölegelendirmek(int 종류, int iş);
    public static native void tamamla_uzakdan_buýruk(int ýagdaý_baha);
    public static native void 원격대기(int ýagdaý_baha);
    public static native void 직렬쓰기(int baha);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int CPU_rugsat_dereje();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int 세로, int 색);
    public static native void togtatmak_CPU();
    public static native int döretmek_tabşyryk(int indeks);
    public static native int tabşyryk_ýagdaý(int indeks);
    public static native void Dur(int ýagdaý_baha);
    public static native int 씨플러스시험();
    public static native int işe_goýber_ulanyjy_programma(int indeks);
    public static native int derňe_ulanyjy_programma();
    public static native int 인수준비(int 개수);
    public static native int ýerine_ýetir_ulanyjy_faýl();
    public static native int 리눅스파일실행();
    public static native int argument_baýt(int indeks, int 위치, int baha);
    public static native int 터미널(int iş);
    public static native int dolandyryş_ulanyjy_programma(int iş);
    public static native void 입출력전환(int iş);
    public static native int faýl_geçir_hyzmat(int iş);
    public static native int Tor_ýagdaý(int girizmeklik_baha, int indeks);
    public static native int Tor_Sazlamalar(int iş, int salgy, int örtük_baha, int şlýuz_baha);
    public static native int 응답보내기(int salgy, int tertip_baha);
    public static native int 응답읽기(int girizmeklik_baha);
    public static native int talap_ulgam(int girizmeklik_baha, int indeks);
    public static native void 전원끄기();
}
