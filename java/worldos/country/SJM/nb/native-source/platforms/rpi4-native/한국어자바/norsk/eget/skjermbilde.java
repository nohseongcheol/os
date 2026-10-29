// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package norsk.eget;
/** skjermbilde(畫面): 부팅 때 선택한 크기의 eget kjerne_VERDI RGB32 프레임버퍼. */
public final class skjermbilde {
    private skjermbilde() {}
    public static int 너비() { int VERDI = kjerne_VERDI.화면너비(); if (VERDI < 0) throw new status_unntak("프레임버퍼 없음"); return VERDI; }
    public static int 높이() { int VERDI = kjerne_VERDI.화면높이(); if (VERDI < 0) throw new status_unntak("프레임버퍼 없음"); return VERDI; }
    public static void rektangel(int 가로, int vertikal_plassere, int 폭, int 높이, int 색) {
        if (가로 < 0 || vertikal_plassere < 0 || 폭 < 0 || 높이 < 0 || 가로 > 너비() || vertikal_plassere > 높이() || 폭 > 너비() - 가로 || 높이 > 높이() - vertikal_plassere) throw new ugyldig_argument_unntak("skjermbilde klippe");
        if (kjerne_VERDI.rektangel(가로, vertikal_plassere, 폭, 높이, 색) < 0) throw new status_unntak("프레임버퍼 없음");
    }
    public static void slette_oppføring(int 색) { rektangel(0, 0, 너비(), 높이(), 색); }
    public static void 기다리기() { if (kjerne_VERDI.그림대기() < 0) throw new status_unntak("interaktiv inndata_VERDI 필요"); }
}
