// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 machine grens_WAARDE. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class Bord {
    public static native int 표시화소읽기(int 가로, int Verticaal_functie);
    public static native void schrijven_weergeven_pixel(int 가로, int Verticaal_functie, int 색);
    public static native int extern_beheer(int soort_WAARDE, int Actie);
    public static native void beëindigen_extern_opdracht(int Status_WAARDE);
    public static native void extern_wachten(int Status_WAARDE);
    public static native void 직렬쓰기(int WAARDE);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int CPU_machtiging_niveau();
    public static native int Bereid_voor_scherm();
    public static native int 화면너비();
    public static native int scherm_hoogte();
    public static native void 화면점(int 가로, int Verticaal_functie, int 색);
    public static native void RENDEMENT_CPU();
    public static native int maken_taak(int INDEX);
    public static native int taak_Status(int INDEX);
    public static native void Stoppen(int Status_WAARDE);
    public static native int 씨플러스시험();
    public static native int uitvoeren_gebruiker_app(int INDEX);
    public static native int cheque_gebruiker_app();
    public static native int 인수준비(int item_AANTAL);
    public static native int Uitvoeren_gebruiker_Bestand();
    public static native int 리눅스파일실행();
    public static native int argument_byte(int INDEX, int positie, int WAARDE);
    public static native int terminal(int Actie);
    public static native int controle_gebruiker_app(int Actie);
    public static native void 입출력전환(int Actie);
    public static native int bestandsoverdracht_service(int Actie);
    public static native int net_status(int invoer_WAARDE_962f286b, int INDEX);
    public static native int net_Instellingen(int Actie, int ADRES, int masker_WAARDE, int gateway_WAARDE);
    public static native int e_mailen_reactie(int ADRES, int order_WAARDE);
    public static native int 응답읽기(int invoer_WAARDE_962f286b);
    public static native int query_Systeem(int invoer_WAARDE_962f286b, int INDEX);
    public static native void 전원끄기();
}
