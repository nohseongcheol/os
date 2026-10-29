// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Türkçe.Öz;
/** 화면(畫面): makine_başlatma 때 선택한 크기의 Öz çekirdek_değer RGB32 프레임버퍼. */
public final class 화면 {
    private 화면() {}
    public static int 너비() { int değer = çekirdek_değer.화면너비(); if (değer < 0) throw new Durum_özel_durum("프레임버퍼 없음"); return değer; }
    public static int 높이() { int değer = çekirdek_değer.화면높이(); if (değer < 0) throw new Durum_özel_durum("프레임버퍼 없음"); return değer; }
    public static void dikdörtgen(int 가로, int Dikey_konum, int 폭, int 높이, int 색) {
        if (가로 < 0 || Dikey_konum < 0 || 폭 < 0 || 높이 < 0 || 가로 > 너비() || Dikey_konum > 높이() || 폭 > 너비() - 가로 || 높이 > 높이() - Dikey_konum) throw new geçersiz_bağımsız_değişken_özel_durum("화면 klip");
        if (çekirdek_değer.dikdörtgen(가로, Dikey_konum, 폭, 높이, 색) < 0) throw new Durum_özel_durum("프레임버퍼 없음");
    }
    public static void silmek_girdi(int 색) { dikdörtgen(0, 0, 너비(), 높이(), 색); }
    public static void 기다리기() { if (çekirdek_değer.그림대기() < 0) throw new Durum_özel_durum("devralmak artış_değer 필요"); }
}
