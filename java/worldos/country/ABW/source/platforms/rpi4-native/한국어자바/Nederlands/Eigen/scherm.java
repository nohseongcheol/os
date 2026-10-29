// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nederlands.Eigen;
/** scherm(畫面): machineopstart 때 선택한 크기의 Eigen kernel_WAARDE RGB32 프레임버퍼. */
public final class scherm {
    private scherm() {}
    public static int 너비() { int WAARDE = kernel_WAARDE.화면너비(); if (WAARDE < 0) throw new Status_uitzondering("프레임버퍼 없음"); return WAARDE; }
    public static int hoogte_WAARDE() { int WAARDE = kernel_WAARDE.scherm_hoogte(); if (WAARDE < 0) throw new Status_uitzondering("프레임버퍼 없음"); return WAARDE; }
    public static void rechthoek(int 가로, int Verticaal_functie, int 폭, int hoogte_WAARDE, int 색) {
        if (가로 < 0 || Verticaal_functie < 0 || 폭 < 0 || hoogte_WAARDE < 0 || 가로 > 너비() || Verticaal_functie > hoogte_WAARDE() || 폭 > 너비() - 가로 || hoogte_WAARDE > hoogte_WAARDE() - Verticaal_functie) throw new nietig_argument_uitzondering("scherm clip");
        if (kernel_WAARDE.rechthoek(가로, Verticaal_functie, 폭, hoogte_WAARDE, 색) < 0) throw new Status_uitzondering("프레임버퍼 없음");
    }
    public static void wissen_invoer(int 색) { rechthoek(0, 0, 너비(), hoogte_WAARDE(), 색); }
    public static void 기다리기() { if (kernel_WAARDE.그림대기() < 0) throw new Status_uitzondering("interactief invoer_WAARDE 필요"); }
}
