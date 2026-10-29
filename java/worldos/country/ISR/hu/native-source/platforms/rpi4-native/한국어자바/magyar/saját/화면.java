// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package magyar.saját;
/** 화면(畫面): 부팅 때 선택한 크기의 saját kernel_ÉRTÉK RGB32 프레임버퍼. */
public final class 화면 {
    private 화면() {}
    public static int 너비() { int ÉRTÉK = kernel_ÉRTÉK.화면너비(); if (ÉRTÉK < 0) throw new Állapot_kivétel("프레임버퍼 없음"); return ÉRTÉK; }
    public static int 높이() { int ÉRTÉK = kernel_ÉRTÉK.화면높이(); if (ÉRTÉK < 0) throw new Állapot_kivétel("프레임버퍼 없음"); return ÉRTÉK; }
    public static void téglalap(int 가로, int szektor_pozíció, int 폭, int 높이, int 색) {
        if (가로 < 0 || szektor_pozíció < 0 || 폭 < 0 || 높이 < 0 || 가로 > 너비() || szektor_pozíció > 높이() || 폭 > 너비() - 가로 || 높이 > 높이() - szektor_pozíció) throw new alaptalan_argumentum_kivétel("화면 klip");
        if (kernel_ÉRTÉK.téglalap(가로, szektor_pozíció, 폭, 높이, 색) < 0) throw new Állapot_kivétel("프레임버퍼 없음");
    }
    public static void töröl_bejegyzés(int 색) { téglalap(0, 0, 너비(), 높이(), 색); }
    public static void 기다리기() { if (kernel_ÉRTÉK.그림대기() < 0) throw new Állapot_kivétel("interaktív bevitel_ÉRTÉK 필요"); }
}
