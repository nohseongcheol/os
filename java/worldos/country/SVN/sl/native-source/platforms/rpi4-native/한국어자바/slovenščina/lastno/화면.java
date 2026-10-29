// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package slovenščina.lastno;
/** 화면(畫面): 부팅 때 선택한 크기의 lastno jedro_VALUE RGB32 프레임버퍼. */
public final class 화면 {
    private 화면() {}
    public static int 너비() { int VALUE = jedro_VALUE.화면너비(); if (VALUE < 0) throw new stanje_izjema("프레임버퍼 없음"); return VALUE; }
    public static int višina_VALUE() { int VALUE = jedro_VALUE.화면높이(); if (VALUE < 0) throw new stanje_izjema("프레임버퍼 없음"); return VALUE; }
    public static void pravokotnik(int 가로, int Navpično_položaj, int 폭, int višina_VALUE, int 색) {
        if (가로 < 0 || Navpično_položaj < 0 || 폭 < 0 || višina_VALUE < 0 || 가로 > 너비() || Navpično_položaj > višina_VALUE() || 폭 > 너비() - 가로 || višina_VALUE > višina_VALUE() - Navpično_položaj) throw new neveljaven_argument_izjema("화면 izrezek");
        if (jedro_VALUE.pravokotnik(가로, Navpično_položaj, 폭, višina_VALUE, 색) < 0) throw new stanje_izjema("프레임버퍼 없음");
    }
    public static void izbrisati_vnos(int 색) { pravokotnik(0, 0, 너비(), višina_VALUE(), 색); }
    public static void 기다리기() { if (jedro_VALUE.그림대기() < 0) throw new stanje_izjema("interaktiven 입력 필요"); }
}
