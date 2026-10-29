// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 maskin 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class Tavle {
    public static native int 표시화소읽기(int 가로, int vertikalvising_plassere);
    public static native void skrive_vise_piksel(int 가로, int vertikalvising_plassere, int 색);
    public static native int skygging(int 종류, int Handling);
    public static native void avslutte_fjern_kommando(int status_VALUE);
    public static native void fjern_vent(int status_VALUE);
    public static native void 직렬쓰기(int VALUE);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int CPU_løyve_nivå();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int vertikalvising_plassere, int 색);
    public static native void YIELD_CPU();
    public static native int Opprett_oppgåve(int INDEX);
    public static native int oppgåve_status(int INDEX);
    public static native void Stopp(int status_VALUE);
    public static native int 씨플러스시험();
    public static native int køyre_brukar_app(int INDEX);
    public static native int sjekk_brukar_app();
    public static native int 인수준비(int vare_COUNT);
    public static native int Utfør_brukar_fil();
    public static native int 리눅스파일실행();
    public static native int argument_byte(int INDEX, int Posisjon, int VALUE);
    public static native int Terminal(int Handling);
    public static native int styring_brukar_app(int Handling);
    public static native void 입출력전환(int Handling);
    public static native int fil_Overfør_teneste(int Handling);
    public static native int Nettverk_merkje(int oppføring_VALUE, int INDEX);
    public static native int Nettverk_Innstillingar(int Handling, int ADDRESS, int maske_VALUE, int gateway_VALUE);
    public static native int 응답보내기(int ADDRESS, int rekkjefølgje_VALUE);
    public static native int 응답읽기(int oppføring_VALUE);
    public static native int spørjing_system(int oppføring_VALUE, int INDEX);
    public static native void 전원끄기();
}
