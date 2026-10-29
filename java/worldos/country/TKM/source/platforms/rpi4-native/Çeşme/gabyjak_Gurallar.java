// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 gabyjak 내장 Gurallar. */
public final class gabyjak_Gurallar {
    static int[] maglumat = new int[16384];
    static int 입력파일 = -1;
    static int aç_faýl(int argument_indeks, int Proses_reje) {
        int 처리값 = 명령해석기.Ýol(argument_indeks); return 처리값 < 0 ? 처리값 : ýat_Faýllar.Aç(Proses_reje);
    }
    static boolean 입력준비(int argument_indeks) {
        입력파일 = -1;
        if (argument_indeks < 명령해석기.토큰수) {
            입력파일 = aç_faýl(argument_indeks, 0);
            if (입력파일 < 0) { 명령해석기.Hata(입력파일); return false; }
        }
        return true;
    }
    static int Oka() {
        if (입력파일 >= 3) return ýat_Faýllar.Oka(입력파일);
        while (true) {
            int baýt_maglumat = 보드.직렬읽기(); if (baýt_maglumat == -2 || baýt_maglumat == 4) return 256;
            if (baýt_maglumat == 3) { 명령해석기.결과 = 130; return 256; }
            if (baýt_maglumat >= 0) return baýt_maglumat; 보드.togtatmak_CPU();
        }
    }
    static void Ýap() { if (입력파일 >= 3) ýat_Faýllar.Ýap(입력파일); 입력파일 = -1; }
    static void görkez_baha() {
        int 마지막자리 = 명령해석기.토큰수 == 1 ? 2 : 명령해석기.토큰수;
        for (int argument_indeks = 1; argument_indeks < 마지막자리; argument_indeks++) {
            if (!입력준비(argument_indeks)) continue;
            int baýt_maglumat; while ((baýt_maglumat = Oka()) != 256 && baýt_maglumat >= 0) 보드.직렬쓰기(baýt_maglumat);
            if (baýt_maglumat < 0) 명령해석기.Hata(baýt_maglumat); Ýap();
        }
    }
    static void faýl_ýumuş(String 동작번호) {
        if (명령해석기.토큰수 != 2) { 명령해석기.결과 = 2; 단말.Ýaz("사용법: mkdir/rmdir/touch Faýl\n"); return; }
        int 처리값 = 명령해석기.Ýol(1);
        if (처리값 >= 0) {
            if (동작번호.charAt(0) == 'm') 처리값 = ýat_Faýllar.döretmek_katalog();
            else if (동작번호.charAt(0) == 'r') 처리값 = ýat_Faýllar.aýyr_katalog();
            else { 처리값 = ýat_Faýllar.Aç(65); if (처리값 >= 3) 처리값 = ýat_Faýllar.Ýap(처리값); }
        }
        if (처리값 < 0) 명령해석기.Hata(처리값);
    }
    static void synp_baha(boolean 이동여부) {
        if (명령해석기.토큰수 != 3) { 명령해석기.결과 = 2; 단말.Ýaz("사용법: cp/mv 원본 목적지 (Faýl)\n"); return; }
        int 처리값 = 명령해석기.Ýol(1); if (처리값 >= 0) 처리값 = ýat_Faýllar.adaty_ýagdaýa_getir_baha();
        if (처리값 < 0) { 명령해석기.Hata(처리값); return; }
        int 원본번호 = ýat_Faýllar.tap_girizmeklik(); if (원본번호 < 0) { 명령해석기.Hata(-2); return; }
        int 항목수 = ýat_Faýllar.dowamlylyk_baha[원본번호]; for (int sikl_indeks = 0; sikl_indeks < 항목수; sikl_indeks++) maglumat[sikl_indeks] = ýat_Faýllar.자료읽기(원본번호, sikl_indeks);
        처리값 = 명령해석기.Ýol(2); if (처리값 >= 0) 처리값 = ýat_Faýllar.adaty_ýagdaýa_getir_baha();
        if (처리값 < 0) { 명령해석기.Hata(처리값); return; }
        if (ýat_Faýllar.tap_girizmeklik() == 원본번호) { if (!이동여부) 명령해석기.Hata(-22); return; }
        if (이동여부) { 처리값 = ýat_Faýllar.이름바꾸기(원본번호); if (처리값 < 0) 명령해석기.Hata(처리값); return; }
        int 열린파일번호 = ýat_Faýllar.Aç(577); if (열린파일번호 < 0) { 명령해석기.Hata(열린파일번호); return; }
        for (int sikl_indeks = 0; sikl_indeks < 항목수; sikl_indeks++) { 처리값 = ýat_Faýllar.Ýaz(열린파일번호, maglumat[sikl_indeks]); if (처리값 < 0) { 명령해석기.Hata(처리값); break; } }
        ýat_Faýllar.Ýap(열린파일번호);
    }
    static int san_baha(int argument_indeks) {
        if (argument_indeks >= 명령해석기.토큰수) return -1;
        int 항목수 = 0; for (int sikl_indeks = 0; sikl_indeks < 명령해석기.dowamlylyk_baha[argument_indeks]; sikl_indeks++) { int nyşanyň_kody = 명령해석기.token_baha[명령해석기.시작점[argument_indeks] + sikl_indeks]; if (nyşanyň_kody < '0' || nyşanyň_kody > '9' || 항목수 > 10000) return -1; 항목수 = 항목수 * 10 + nyşanyň_kody - '0'; } return 항목수;
    }
    static void 세기() {
        int argument_indeks = 1, opsiýa = 0;
        if (명령해석기.같음(1, "-c") || 명령해석기.같음(1, "-l") || 명령해석기.같음(1, "-w")) { opsiýa = 명령해석기.같음(1, "-c") ? 1 : 명령해석기.같음(1, "-l") ? 2 : 3; argument_indeks++; }
        if (명령해석기.토큰수 > argument_indeks + 1) { 명령해석기.결과 = 2; 단말.Ýaz("사용법: wc [-c|-l|-w] [Faýl]\n"); return; }
        if (!입력준비(argument_indeks)) return;
        int 바이트수 = 0, 줄수 = 0, 낱말수 = 0, baýt_maglumat; boolean 낱말 = false;
        while ((baýt_maglumat = Oka()) >= 0 && baýt_maglumat != 256) { 바이트수++; if (baýt_maglumat == 10) 줄수++; boolean ýer = baýt_maglumat == 32 || baýt_maglumat >= 9 && baýt_maglumat <= 13; if (!ýer && !낱말) 낱말수++; 낱말 = !ýer; }
        Ýap(); if (baýt_maglumat < 0) { 명령해석기.Hata(baýt_maglumat); return; }
        if (opsiýa != 0) 단말.수(opsiýa == 1 ? 바이트수 : opsiýa == 2 ? 줄수 : 낱말수);
        else { 단말.수(줄수); 단말.문자(' '); 단말.수(낱말수); 단말.문자(' '); 단말.수(바이트수); } 단말.문자(10);
    }
    static void tap_girizmeklik() {
        if (명령해석기.토큰수 < 2 || 명령해석기.토큰수 > 3) { 명령해석기.결과 = 2; 단말.Ýaz("사용법: grep 찾을문구 [Faýl]\n"); return; }
        if (!입력준비(2)) return;
        int 항목수 = 0, baýt_maglumat, 일치수 = 0;
        while (true) {
            baýt_maglumat = Oka();
            if (baýt_maglumat == 10 || baýt_maglumat == 256 || baýt_maglumat < 0) {
                boolean 찾은여부 = false;
                for (int sikl_indeks = 0; sikl_indeks <= 항목수 - 명령해석기.dowamlylyk_baha[1]; sikl_indeks++) {
                    boolean 같은여부 = true; for (int 안쪽자리 = 0; 안쪽자리 < 명령해석기.dowamlylyk_baha[1]; 안쪽자리++) if (maglumat[sikl_indeks + 안쪽자리] != 명령해석기.token_baha[명령해석기.시작점[1] + 안쪽자리]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (항목수 > 0 || baýt_maglumat == 10)) { for (int sikl_indeks = 0; sikl_indeks < 항목수; sikl_indeks++) 보드.직렬쓰기(maglumat[sikl_indeks]); 단말.문자(10); 일치수++; }
                항목수 = 0; if (baýt_maglumat != 10) break;
            } else if (항목수 < maglumat.length) maglumat[항목수++] = baýt_maglumat;
            else { 명령해석기.Hata(-28); Ýap(); return; }
        }
        Ýap(); if (baýt_maglumat < 0) 명령해석기.Hata(baýt_maglumat); else if (명령해석기.결과 == 0) 명령해석기.결과 = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int argument_indeks = 1, 줄수 = 10;
        if (명령해석기.같음(1, "-n")) { 줄수 = san_baha(2); argument_indeks = 3; }
        if (줄수 < 0 || 명령해석기.토큰수 > argument_indeks + 1) { 명령해석기.결과 = 2; 단말.Ýaz("사용법: head/tail [-n 줄수] [Faýl]\n"); return; }
        if (!입력준비(argument_indeks)) return;
        int 항목수 = 0, baýt_maglumat;
        while ((baýt_maglumat = Oka()) != 256 && baýt_maglumat >= 0) { if (항목수 == maglumat.length) { 명령해석기.Hata(-28); Ýap(); return; } maglumat[항목수++] = baýt_maglumat; }
        Ýap(); if (baýt_maglumat < 0) { 명령해석기.Hata(baýt_maglumat); return; }
        int ýerli_başlat = 0, 끝자리 = 항목수;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int 총수 = 0; for (int sikl_indeks = 항목수 - 2; sikl_indeks >= 0; sikl_indeks--) if (maglumat[sikl_indeks] == 10 && ++총수 == 줄수) { ýerli_başlat = sikl_indeks + 1; break; } }
        else { int 총수 = 0; for (int sikl_indeks = 0; sikl_indeks < 항목수; sikl_indeks++) if (maglumat[sikl_indeks] == 10 && ++총수 == 줄수) { 끝자리 = sikl_indeks + 1; break; } }
        for (int sikl_indeks = ýerli_başlat; sikl_indeks < 끝자리; sikl_indeks++) 보드.직렬쓰기(maglumat[sikl_indeks]);
    }
    static void 함께쓰기() {
        boolean 덧붙임여부 = 명령해석기.같음(1, "-a"); int argument_indeks = 덧붙임여부 ? 2 : 1;
        if (명령해석기.토큰수 != argument_indeks + 1) { 명령해석기.결과 = 2; 단말.Ýaz("사용법: tee [-a] Faýl\n"); return; }
        int 열린파일번호 = aç_faýl(argument_indeks, 덧붙임여부 ? 1089 : 577); if (열린파일번호 < 0) { 명령해석기.Hata(열린파일번호); return; }
        입력파일 = -1; int baýt_maglumat;
        while ((baýt_maglumat = Oka()) != 256 && baýt_maglumat >= 0) { int 처리값 = ýat_Faýllar.Ýaz(열린파일번호, baýt_maglumat); if (처리값 < 0) { 명령해석기.Hata(처리값); break; } 보드.직렬쓰기(baýt_maglumat); }
        ýat_Faýllar.Ýap(열린파일번호);
    }
}
