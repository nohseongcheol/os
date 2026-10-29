// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package polski.własny;
/** 화면(畫面): rozruch_maszyny 때 선택한 크기의 własny jądro_WARTOŚĆ RGB32 프레임버퍼. */
public final class 화면 {
    private 화면() {}
    public static int 너비() { int WARTOŚĆ = jądro_WARTOŚĆ.화면너비(); if (WARTOŚĆ < 0) throw new Stan_wyjątek("프레임버퍼 없음"); return WARTOŚĆ; }
    public static int wysokość_WARTOŚĆ() { int WARTOŚĆ = jądro_WARTOŚĆ.화면높이(); if (WARTOŚĆ < 0) throw new Stan_wyjątek("프레임버퍼 없음"); return WARTOŚĆ; }
    public static void prostokąt(int 가로, int gałąź_stanowisko, int 폭, int wysokość_WARTOŚĆ, int 색) {
        if (가로 < 0 || gałąź_stanowisko < 0 || 폭 < 0 || wysokość_WARTOŚĆ < 0 || 가로 > 너비() || gałąź_stanowisko > wysokość_WARTOŚĆ() || 폭 > 너비() - 가로 || wysokość_WARTOŚĆ > wysokość_WARTOŚĆ() - gałąź_stanowisko) throw new nieważny_argument_wyjątek("화면 obcinać");
        if (jądro_WARTOŚĆ.prostokąt(가로, gałąź_stanowisko, 폭, wysokość_WARTOŚĆ, 색) < 0) throw new Stan_wyjątek("프레임버퍼 없음");
    }
    public static void usunąć_wpis(int 색) { prostokąt(0, 0, 너비(), wysokość_WARTOŚĆ(), 색); }
    public static void 기다리기() { if (jądro_WARTOŚĆ.그림대기() < 0) throw new Stan_wyjątek("interakcyjny wejście_WARTOŚĆ 필요"); }
}
