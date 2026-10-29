// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 maskin grense_VERDI. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class Tavle {
    public static native int 표시화소읽기(int 가로, int vertikal_plassere);
    public static native void skrive_vise_piksel(int 가로, int vertikal_plassere, int 색);
    public static native int skygging(int 종류, int Handling);
    public static native void avslutte_en_samtale_ekstern_kommando(int status_VERDI);
    public static native void ekstern_vent(int status_VERDI);
    public static native void 직렬쓰기(int VERDI);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int CPU_rettighet_nivå();
    public static native int Forbered_skjermbilde();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int vertikal_plassere, int 색);
    public static native void AVKAST_CPU();
    public static native int åpne_oppgave(int INDEKS);
    public static native int oppgave_status(int INDEKS);
    public static native void Stopp(int status_VERDI);
    public static native int 씨플러스시험();
    public static native int kjøre_bruker_app(int INDEKS);
    public static native int sjekk_bruker_app();
    public static native int 인수준비(int vare_ANTALL);
    public static native int Utfør_bruker_Fil();
    public static native int 리눅스파일실행();
    public static native int argument_byte(int INDEKS, int Posisjon, int VERDI);
    public static native int Terminal(int Handling);
    public static native int kontroll_bruker_app(int Handling);
    public static native void 입출력전환(int Handling);
    public static native int filoverføring_service(int Handling);
    public static native int nettverk_status(int oppføring_VERDI, int INDEKS);
    public static native int nettverk_Innstillinger(int Handling, int e_post, int maske_VERDI, int gateway_VERDI);
    public static native int sende_svar(int e_post, int ordre_VERDI);
    public static native int 응답읽기(int oppføring_VERDI);
    public static native int spørre_System(int oppføring_VERDI, int INDEKS);
    public static native void 전원끄기();
}
