// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 화면(畫面): 부팅 때 선택한 크기의 자체 ядро_мән RGB32 프레임버퍼. */
public final class 화면 {
    private 화면() {}
    public static int 너비() { int мән = ядро_мән.화면너비(); if (мән < 0) throw new күй_ерекшелік("프레임버퍼 없음"); return мән; }
    public static int 높이() { int мән = ядро_мән.화면높이(); if (мән < 0) throw new күй_ерекшелік("프레임버퍼 없음"); return мән; }
    public static void тік_төртбұрыш(int 가로, int Тік_лауазым, int 폭, int 높이, int 색) {
        if (가로 < 0 || Тік_лауазым < 0 || 폭 < 0 || 높이 < 0 || 가로 > 너비() || Тік_лауазым > 높이() || 폭 > 너비() - 가로 || 높이 > 높이() - Тік_лауазым) throw new дұрыс_емес_аргумент_ерекшелік("화면 клип");
        if (ядро_мән.тік_төртбұрыш(가로, Тік_лауазым, 폭, 높이, 색) < 0) throw new күй_ерекшелік("프레임버퍼 없음");
    }
    public static void өшіру_енгізу(int 색) { тік_төртбұрыш(0, 0, 너비(), 높이(), 색); }
    public static void 기다리기() { if (ядро_мән.그림대기() < 0) throw new күй_ерекшелік("көзбе_көз_белсенді 입력 필요"); }
}
