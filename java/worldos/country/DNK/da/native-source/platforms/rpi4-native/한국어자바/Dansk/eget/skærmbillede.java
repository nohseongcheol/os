// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Dansk.eget;
/** skærmbillede(畫面): 부팅 때 선택한 크기의 eget kerne_VÆRDI RGB32 프레임버퍼. */
public final class skærmbillede {
    private skærmbillede() {}
    public static int 너비() { int VÆRDI = kerne_VÆRDI.화면너비(); if (VÆRDI < 0) throw new status_undtagelse("프레임버퍼 없음"); return VÆRDI; }
    public static int 높이() { int VÆRDI = kerne_VÆRDI.화면높이(); if (VÆRDI < 0) throw new status_undtagelse("프레임버퍼 없음"); return VÆRDI; }
    public static void rektangel(int 가로, int Lodret_placere, int 폭, int 높이, int 색) {
        if (가로 < 0 || Lodret_placere < 0 || 폭 < 0 || 높이 < 0 || 가로 > 너비() || Lodret_placere > 높이() || 폭 > 너비() - 가로 || 높이 > 높이() - Lodret_placere) throw new ugyldig_argument_undtagelse("skærmbillede klippe");
        if (kerne_VÆRDI.rektangel(가로, Lodret_placere, 폭, 높이, 색) < 0) throw new status_undtagelse("프레임버퍼 없음");
    }
    public static void slette_post(int 색) { rektangel(0, 0, 너비(), 높이(), 색); }
    public static void 기다리기() { if (kerne_VÆRDI.그림대기() < 0) throw new status_undtagelse("interaktiv input_VÆRDI 필요"); }
}
