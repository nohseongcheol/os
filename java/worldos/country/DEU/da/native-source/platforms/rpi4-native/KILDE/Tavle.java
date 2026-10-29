// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 maskine grænse_VÆRDI. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class Tavle {
    public static native int 표시화소읽기(int 가로, int Lodret_placere);
    public static native void skrive_vise_pixel(int 가로, int Lodret_placere, int 색);
    public static native int skygning(int 종류, int Handling);
    public static native void afslutte_et_opkald_fjern_kommando(int status_VÆRDI);
    public static native void fjern_vent(int status_VÆRDI);
    public static native void 직렬쓰기(int VÆRDI);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int CPU_rettighed_vater();
    public static native int Tilrettelæg_skærmbillede();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int Lodret_placere, int 색);
    public static native void AFKAST_CPU();
    public static native int åbne_job(int INDEKS);
    public static native int job_status(int INDEKS);
    public static native void Stop(int status_VÆRDI);
    public static native int 씨플러스시험();
    public static native int køre_bruger_app(int INDEKS);
    public static native int check_bruger_app();
    public static native int 인수준비(int vare_TÆL);
    public static native int Udfør_bruger_fil();
    public static native int 리눅스파일실행();
    public static native int argument_byte(int INDEKS, int Placering, int VÆRDI);
    public static native int Terminal(int Handling);
    public static native int kontrol_bruger_app(int Handling);
    public static native void 입출력전환(int Handling);
    public static native int filoverførsel_service(int Handling);
    public static native int netværk_status(int post_VÆRDI_962f286b, int INDEKS);
    public static native int netværk_Indstillinger(int Handling, int mail, int maske_VÆRDI, int gateway_VÆRDI);
    public static native int maile_svar(int mail, int ordre_VÆRDI);
    public static native int 응답읽기(int post_VÆRDI_962f286b);
    public static native int forespørge_System(int post_VÆRDI_962f286b, int INDEKS);
    public static native void 전원끄기();
}
