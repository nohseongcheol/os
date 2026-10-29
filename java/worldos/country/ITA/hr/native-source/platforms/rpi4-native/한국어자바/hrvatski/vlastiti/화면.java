// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package hrvatski.vlastiti;
/** 화면(畫面): 부팅 때 선택한 크기의 vlastiti jezgra_sustava_VALUE RGB32 프레임버퍼. */
public final class 화면 {
    private 화면() {}
    public static int 너비() { int VALUE = jezgra_sustava_VALUE.화면너비(); if (VALUE < 0) throw new Stanje_iznimka("프레임버퍼 없음"); return VALUE; }
    public static int 높이() { int VALUE = jezgra_sustava_VALUE.화면높이(); if (VALUE < 0) throw new Stanje_iznimka("프레임버퍼 없음"); return VALUE; }
    public static void pravokutnik(int 가로, int Okomito_položaj, int 폭, int 높이, int 색) {
        if (가로 < 0 || Okomito_položaj < 0 || 폭 < 0 || 높이 < 0 || 가로 > 너비() || Okomito_položaj > 높이() || 폭 > 너비() - 가로 || 높이 > 높이() - Okomito_položaj) throw new nevaljan_argument_iznimka("화면 isječak");
        if (jezgra_sustava_VALUE.pravokutnik(가로, Okomito_položaj, 폭, 높이, 색) < 0) throw new Stanje_iznimka("프레임버퍼 없음");
    }
    public static void izbrisati_unos(int 색) { pravokutnik(0, 0, 너비(), 높이(), 색); }
    public static void 기다리기() { if (jezgra_sustava_VALUE.그림대기() < 0) throw new Stanje_iznimka("대화형 입력 필요"); }
}
