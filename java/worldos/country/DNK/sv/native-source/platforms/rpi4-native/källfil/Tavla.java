// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 dator gräns_värde. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class Tavla {
    public static native int läsa_visa_bildpunkt(int 가로, int bransch_placera);
    public static native void skriva_visa_bildpunkt(int 가로, int bransch_placera, int 색);
    public static native int skuggning(int variant_värde, int Åtgärd);
    public static native void avsluta_fjärr_kommando(int status_värde);
    public static native void fjärr_vänta(int status_värde);
    public static native void 직렬쓰기(int värde);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int CPU_behörighet_nivå();
    public static native int Förbereda_skärmbild();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int bransch_placera, int 색);
    public static native void NOMAVK_CPU();
    public static native int Skapa_uppgift(int INDEX);
    public static native int uppgift_status(int INDEX);
    public static native void Stopp(int status_värde);
    public static native int 씨플러스시험();
    public static native int köra_användare_app(int INDEX);
    public static native int check_användare_app();
    public static native int 인수준비(int objekt_ANTAL);
    public static native int köra_användare_fil();
    public static native int 리눅스파일실행();
    public static native int argument_byte(int INDEX, int position, int värde);
    public static native int kommandotolk(int Åtgärd);
    public static native int kontroll_användare_app(int Åtgärd);
    public static native void 입출력전환(int Åtgärd);
    public static native int filöverföring_tjänst(int Åtgärd);
    public static native int nätverk_status(int post_värde, int INDEX);
    public static native int nätverk_Inställningar(int Åtgärd, int Adress, int mask_värde, int gateway_värde);
    public static native int skicka_svar(int Adress, int order_värde);
    public static native int läsa_svar(int post_värde);
    public static native int fråga_System(int post_värde, int INDEX);
    public static native void 전원끄기();
}
