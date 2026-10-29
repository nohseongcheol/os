// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 kabuk 내장 araçlar. */
public final class kabuk_Araçlar {
    static int[] veri = new int[16384];
    static int giriş_dosyası = -1;
    static int açık_Dosya(int bağımsız_değişken_Dizin, int işlem_mod) {
        int 처리값 = KomutYorumlayıcı.yol(bağımsız_değişken_Dizin); return 처리값 < 0 ? 처리값 : BellekDosyaları.Aç(işlem_mod);
    }
    static boolean Hazırlan_artış(int bağımsız_değişken_Dizin) {
        giriş_dosyası = -1;
        if (bağımsız_değişken_Dizin < KomutYorumlayıcı.belirteç_BAĞ_DEĞ_SAY) {
            giriş_dosyası = açık_Dosya(bağımsız_değişken_Dizin, 0);
            if (giriş_dosyası < 0) { KomutYorumlayıcı.hata(giriş_dosyası); return false; }
        }
        return true;
    }
    static int Okuma() {
        if (giriş_dosyası >= 3) return BellekDosyaları.Okuma(giriş_dosyası);
        while (true) {
            int bayt_veri = Pano.직렬읽기(); if (bayt_veri == -2 || bayt_veri == 4) return 256;
            if (bayt_veri == 3) { KomutYorumlayıcı.sonuç = 130; return 256; }
            if (bayt_veri >= 0) return bayt_veri; Pano.ÖDEME_CPU();
        }
    }
    static void Kapat() { if (giriş_dosyası >= 3) BellekDosyaları.Kapat(giriş_dosyası); giriş_dosyası = -1; }
    static void Görünüm_değer() {
        int 마지막자리 = KomutYorumlayıcı.belirteç_BAĞ_DEĞ_SAY == 1 ? 2 : KomutYorumlayıcı.belirteç_BAĞ_DEĞ_SAY;
        for (int bağımsız_değişken_Dizin = 1; bağımsız_değişken_Dizin < 마지막자리; bağımsız_değişken_Dizin++) {
            if (!Hazırlan_artış(bağımsız_değişken_Dizin)) continue;
            int bayt_veri; while ((bayt_veri = Okuma()) != 256 && bayt_veri >= 0) Pano.직렬쓰기(bayt_veri);
            if (bayt_veri < 0) KomutYorumlayıcı.hata(bayt_veri); Kapat();
        }
    }
    static void Dosya_iş(String 동작번호) {
        if (KomutYorumlayıcı.belirteç_BAĞ_DEĞ_SAY != 2) { KomutYorumlayıcı.sonuç = 2; 단말.Yazma("사용법: mkdir/rmdir/touch dosya\n"); return; }
        int 처리값 = KomutYorumlayıcı.yol(1);
        if (처리값 >= 0) {
            if (동작번호.charAt(0) == 'm') 처리값 = BellekDosyaları.açmak_dizin();
            else if (동작번호.charAt(0) == 'r') 처리값 = BellekDosyaları.kaldırmak_dizin();
            else { 처리값 = BellekDosyaları.Aç(65); if (처리값 >= 3) 처리값 = BellekDosyaları.Kapat(처리값); }
        }
        if (처리값 < 0) KomutYorumlayıcı.hata(처리값);
    }
    static void örnek_değer(boolean 이동여부) {
        if (KomutYorumlayıcı.belirteç_BAĞ_DEĞ_SAY != 3) { KomutYorumlayıcı.sonuç = 2; 단말.Yazma("사용법: cp/mv 원본 hedef_uç_nokta (dosya)\n"); return; }
        int 처리값 = KomutYorumlayıcı.yol(1); if (처리값 >= 0) 처리값 = BellekDosyaları.normalleştirmek_değer();
        if (처리값 < 0) { KomutYorumlayıcı.hata(처리값); return; }
        int 원본번호 = BellekDosyaları.BUL_girdi(); if (원본번호 < 0) { KomutYorumlayıcı.hata(-2); return; }
        int girdi_BAĞ_DEĞ_SAY = BellekDosyaları.süre_değer[원본번호]; for (int Loop_Dizin = 0; Loop_Dizin < girdi_BAĞ_DEĞ_SAY; Loop_Dizin++) veri[Loop_Dizin] = BellekDosyaları.자료읽기(원본번호, Loop_Dizin);
        처리값 = KomutYorumlayıcı.yol(2); if (처리값 >= 0) 처리값 = BellekDosyaları.normalleştirmek_değer();
        if (처리값 < 0) { KomutYorumlayıcı.hata(처리값); return; }
        if (BellekDosyaları.BUL_girdi() == 원본번호) { if (!이동여부) KomutYorumlayıcı.hata(-22); return; }
        if (이동여부) { 처리값 = BellekDosyaları.Yeniden_Adlandır_girdi(원본번호); if (처리값 < 0) KomutYorumlayıcı.hata(처리값); return; }
        int 열린파일번호 = BellekDosyaları.Aç(577); if (열린파일번호 < 0) { KomutYorumlayıcı.hata(열린파일번호); return; }
        for (int Loop_Dizin = 0; Loop_Dizin < girdi_BAĞ_DEĞ_SAY; Loop_Dizin++) { 처리값 = BellekDosyaları.Yazma(열린파일번호, veri[Loop_Dizin]); if (처리값 < 0) { KomutYorumlayıcı.hata(처리값); break; } }
        BellekDosyaları.Kapat(열린파일번호);
    }
    static int rakam_değer(int bağımsız_değişken_Dizin) {
        if (bağımsız_değişken_Dizin >= KomutYorumlayıcı.belirteç_BAĞ_DEĞ_SAY) return -1;
        int girdi_BAĞ_DEĞ_SAY = 0; for (int Loop_Dizin = 0; Loop_Dizin < KomutYorumlayıcı.süre_değer[bağımsız_değişken_Dizin]; Loop_Dizin++) { int kod_noktası = KomutYorumlayıcı.belirteç_değer[KomutYorumlayıcı.시작점[bağımsız_değişken_Dizin] + Loop_Dizin]; if (kod_noktası < '0' || kod_noktası > '9' || girdi_BAĞ_DEĞ_SAY > 10000) return -1; girdi_BAĞ_DEĞ_SAY = girdi_BAĞ_DEĞ_SAY * 10 + kod_noktası - '0'; } return girdi_BAĞ_DEĞ_SAY;
    }
    static void 세기() {
        int bağımsız_değişken_Dizin = 1, 선택번호 = 0;
        if (KomutYorumlayıcı.같음(1, "-c") || KomutYorumlayıcı.같음(1, "-l") || KomutYorumlayıcı.같음(1, "-w")) { 선택번호 = KomutYorumlayıcı.같음(1, "-c") ? 1 : KomutYorumlayıcı.같음(1, "-l") ? 2 : 3; bağımsız_değişken_Dizin++; }
        if (KomutYorumlayıcı.belirteç_BAĞ_DEĞ_SAY > bağımsız_değişken_Dizin + 1) { KomutYorumlayıcı.sonuç = 2; 단말.Yazma("사용법: wc [-c|-l|-w] [dosya]\n"); return; }
        if (!Hazırlan_artış(bağımsız_değişken_Dizin)) return;
        int bayt_BAĞ_DEĞ_SAY = 0, 줄수 = 0, 낱말수 = 0, bayt_veri; boolean 낱말 = false;
        while ((bayt_veri = Okuma()) >= 0 && bayt_veri != 256) { bayt_BAĞ_DEĞ_SAY++; if (bayt_veri == 10) 줄수++; boolean yer = bayt_veri == 32 || bayt_veri >= 9 && bayt_veri <= 13; if (!yer && !낱말) 낱말수++; 낱말 = !yer; }
        Kapat(); if (bayt_veri < 0) { KomutYorumlayıcı.hata(bayt_veri); return; }
        if (선택번호 != 0) 단말.수(선택번호 == 1 ? bayt_BAĞ_DEĞ_SAY : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.수(줄수); 단말.문자(' '); 단말.수(낱말수); 단말.문자(' '); 단말.수(bayt_BAĞ_DEĞ_SAY); } 단말.문자(10);
    }
    static void BUL_girdi() {
        if (KomutYorumlayıcı.belirteç_BAĞ_DEĞ_SAY < 2 || KomutYorumlayıcı.belirteç_BAĞ_DEĞ_SAY > 3) { KomutYorumlayıcı.sonuç = 2; 단말.Yazma("사용법: grep 찾을문구 [dosya]\n"); return; }
        if (!Hazırlan_artış(2)) return;
        int girdi_BAĞ_DEĞ_SAY = 0, bayt_veri, 일치수 = 0;
        while (true) {
            bayt_veri = Okuma();
            if (bayt_veri == 10 || bayt_veri == 256 || bayt_veri < 0) {
                boolean 찾은여부 = false;
                for (int Loop_Dizin = 0; Loop_Dizin <= girdi_BAĞ_DEĞ_SAY - KomutYorumlayıcı.süre_değer[1]; Loop_Dizin++) {
                    boolean 같은여부 = true; for (int iç_konum = 0; iç_konum < KomutYorumlayıcı.süre_değer[1]; iç_konum++) if (veri[Loop_Dizin + iç_konum] != KomutYorumlayıcı.belirteç_değer[KomutYorumlayıcı.시작점[1] + iç_konum]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (girdi_BAĞ_DEĞ_SAY > 0 || bayt_veri == 10)) { for (int Loop_Dizin = 0; Loop_Dizin < girdi_BAĞ_DEĞ_SAY; Loop_Dizin++) Pano.직렬쓰기(veri[Loop_Dizin]); 단말.문자(10); 일치수++; }
                girdi_BAĞ_DEĞ_SAY = 0; if (bayt_veri != 10) break;
            } else if (girdi_BAĞ_DEĞ_SAY < veri.length) veri[girdi_BAĞ_DEĞ_SAY++] = bayt_veri;
            else { KomutYorumlayıcı.hata(-28); Kapat(); return; }
        }
        Kapat(); if (bayt_veri < 0) KomutYorumlayıcı.hata(bayt_veri); else if (KomutYorumlayıcı.sonuç == 0) KomutYorumlayıcı.sonuç = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int bağımsız_değişken_Dizin = 1, 줄수 = 10;
        if (KomutYorumlayıcı.같음(1, "-n")) { 줄수 = rakam_değer(2); bağımsız_değişken_Dizin = 3; }
        if (줄수 < 0 || KomutYorumlayıcı.belirteç_BAĞ_DEĞ_SAY > bağımsız_değişken_Dizin + 1) { KomutYorumlayıcı.sonuç = 2; 단말.Yazma("사용법: head/tail [-n 줄수] [dosya]\n"); return; }
        if (!Hazırlan_artış(bağımsız_değişken_Dizin)) return;
        int girdi_BAĞ_DEĞ_SAY = 0, bayt_veri;
        while ((bayt_veri = Okuma()) != 256 && bayt_veri >= 0) { if (girdi_BAĞ_DEĞ_SAY == veri.length) { KomutYorumlayıcı.hata(-28); Kapat(); return; } veri[girdi_BAĞ_DEĞ_SAY++] = bayt_veri; }
        Kapat(); if (bayt_veri < 0) { KomutYorumlayıcı.hata(bayt_veri); return; }
        int yerel_Start = 0, Bitiş_konum = girdi_BAĞ_DEĞ_SAY;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int toplam_BAĞ_DEĞ_SAY = 0; for (int Loop_Dizin = girdi_BAĞ_DEĞ_SAY - 2; Loop_Dizin >= 0; Loop_Dizin--) if (veri[Loop_Dizin] == 10 && ++toplam_BAĞ_DEĞ_SAY == 줄수) { yerel_Start = Loop_Dizin + 1; break; } }
        else { int toplam_BAĞ_DEĞ_SAY = 0; for (int Loop_Dizin = 0; Loop_Dizin < girdi_BAĞ_DEĞ_SAY; Loop_Dizin++) if (veri[Loop_Dizin] == 10 && ++toplam_BAĞ_DEĞ_SAY == 줄수) { Bitiş_konum = Loop_Dizin + 1; break; } }
        for (int Loop_Dizin = yerel_Start; Loop_Dizin < Bitiş_konum; Loop_Dizin++) Pano.직렬쓰기(veri[Loop_Dizin]);
    }
    static void yazma_Birlikte() {
        boolean Ekleme = KomutYorumlayıcı.같음(1, "-a"); int bağımsız_değişken_Dizin = Ekleme ? 2 : 1;
        if (KomutYorumlayıcı.belirteç_BAĞ_DEĞ_SAY != bağımsız_değişken_Dizin + 1) { KomutYorumlayıcı.sonuç = 2; 단말.Yazma("사용법: tee [-a] dosya\n"); return; }
        int 열린파일번호 = açık_Dosya(bağımsız_değişken_Dizin, Ekleme ? 1089 : 577); if (열린파일번호 < 0) { KomutYorumlayıcı.hata(열린파일번호); return; }
        giriş_dosyası = -1; int bayt_veri;
        while ((bayt_veri = Okuma()) != 256 && bayt_veri >= 0) { int 처리값 = BellekDosyaları.Yazma(열린파일번호, bayt_veri); if (처리값 < 0) { KomutYorumlayıcı.hata(처리값); break; } Pano.직렬쓰기(bayt_veri); }
        BellekDosyaları.Kapat(열린파일번호);
    }
}
