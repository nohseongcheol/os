// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Svenska.eget;
/** skärmbild(畫面): maskinstart 때 선택한 크기의 eget kärna_värde RGB32 프레임버퍼. */
public final class skärmbild {
    private skärmbild() {}
    public static int 너비() { int värde = kärna_värde.화면너비(); if (värde < 0) throw new status_fel("프레임버퍼 없음"); return värde; }
    public static int 높이() { int värde = kärna_värde.화면높이(); if (värde < 0) throw new status_fel("프레임버퍼 없음"); return värde; }
    public static void rektangel(int 가로, int bransch_placera, int 폭, int 높이, int 색) {
        if (가로 < 0 || bransch_placera < 0 || 폭 < 0 || 높이 < 0 || 가로 > 너비() || bransch_placera > 높이() || 폭 > 너비() - 가로 || 높이 > 높이() - bransch_placera) throw new ogiltig_argument_fel("skärmbild klipp");
        if (kärna_värde.rektangel(가로, bransch_placera, 폭, 높이, 색) < 0) throw new status_fel("프레임버퍼 없음");
    }
    public static void radera_post(int 색) { rektangel(0, 0, 너비(), 높이(), 색); }
    public static void 기다리기() { if (kärna_värde.그림대기() < 0) throw new status_fel("interaktiv indata_värde 필요"); }
}
