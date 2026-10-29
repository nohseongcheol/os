// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latviešu.savs;
/** 화면(畫面): 부팅 때 선택한 크기의 savs kodols_VALUE RGB32 프레임버퍼. */
public final class 화면 {
    private 화면() {}
    public static int 너비() { int VALUE = kodols_VALUE.화면너비(); if (VALUE < 0) throw new Statuss_izņēmums("프레임버퍼 없음"); return VALUE; }
    public static int 높이() { int VALUE = kodols_VALUE.화면높이(); if (VALUE < 0) throw new Statuss_izņēmums("프레임버퍼 없음"); return VALUE; }
    public static void taisnstūris(int 가로, int vertikāle_amats, int 폭, int 높이, int 색) {
        if (가로 < 0 || vertikāle_amats < 0 || 폭 < 0 || 높이 < 0 || 가로 > 너비() || vertikāle_amats > 높이() || 폭 > 너비() - 가로 || 높이 > 높이() - vertikāle_amats) throw new nederīgs_arg_izņēmums("화면 klips");
        if (kodols_VALUE.taisnstūris(가로, vertikāle_amats, 폭, 높이, 색) < 0) throw new Statuss_izņēmums("프레임버퍼 없음");
    }
    public static void dzēst_ievade(int 색) { taisnstūris(0, 0, 너비(), 높이(), 색); }
    public static void 기다리기() { if (kodols_VALUE.그림대기() < 0) throw new Statuss_izņēmums("대화형 입력 필요"); }
}
