// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 setlhalosataelo 내장 Thuluse. */
public final class setlhalosataelo_Thuluse {
    static int[] tshedimosetso = new int[16384];
    static int 입력파일 = -1;
    static int bula_faele(int Thulaganyo_tshupane, int Thulaganyo_mokgwa) {
        int 처리값 = 명령해석기.tsela(Thulaganyo_tshupane); return 처리값 < 0 ? 처리값 : memori_Difaele.bula(Thulaganyo_mokgwa);
    }
    static boolean 입력준비(int Thulaganyo_tshupane) {
        입력파일 = -1;
        if (Thulaganyo_tshupane < 명령해석기.토큰수) {
            입력파일 = bula_faele(Thulaganyo_tshupane, 0);
            if (입력파일 < 0) { 명령해석기.phoso(입력파일); return false; }
        }
        return true;
    }
    static int 읽기() {
        if (입력파일 >= 3) return memori_Difaele.읽기(입력파일);
        while (true) {
            int baete_tshedimosetso = 보드.직렬읽기(); if (baete_tshedimosetso == -2 || baete_tshedimosetso == 4) return 256;
            if (baete_tshedimosetso == 3) { 명령해석기.결과 = 130; return 256; }
            if (baete_tshedimosetso >= 0) return baete_tshedimosetso; 보드.emisa_ka_nakwana_CPU();
        }
    }
    static void tswala() { if (입력파일 >= 3) memori_Difaele.tswala(입력파일); 입력파일 = -1; }
    static void Tebego_Boleng() {
        int 마지막자리 = 명령해석기.토큰수 == 1 ? 2 : 명령해석기.토큰수;
        for (int Thulaganyo_tshupane = 1; Thulaganyo_tshupane < 마지막자리; Thulaganyo_tshupane++) {
            if (!입력준비(Thulaganyo_tshupane)) continue;
            int baete_tshedimosetso; while ((baete_tshedimosetso = 읽기()) != 256 && baete_tshedimosetso >= 0) 보드.직렬쓰기(baete_tshedimosetso);
            if (baete_tshedimosetso < 0) 명령해석기.phoso(baete_tshedimosetso); tswala();
        }
    }
    static void faele_Tiro(String 동작번호) {
        if (명령해석기.토큰수 != 2) { 명령해석기.결과 = 2; 단말.kwala("사용법: mkdir/rmdir/touch faele\n"); return; }
        int 처리값 = 명령해석기.tsela(1);
        if (처리값 >= 0) {
            if (동작번호.charAt(0) == 'm') 처리값 = memori_Difaele.tlhama_Lenaneofaele();
            else if (동작번호.charAt(0) == 'r') 처리값 = memori_Difaele.tlosa_Lenaneofaele();
            else { 처리값 = memori_Difaele.bula(65); if (처리값 >= 3) 처리값 = memori_Difaele.tswala(처리값); }
        }
        if (처리값 < 0) 명령해석기.phoso(처리값);
    }
    static void leloko_Boleng(boolean 이동여부) {
        if (명령해석기.토큰수 != 3) { 명령해석기.결과 = 2; 단말.kwala("사용법: cp/mv 원본 목적지 (faele)\n"); return; }
        int 처리값 = 명령해석기.tsela(1); if (처리값 >= 0) 처리값 = memori_Difaele.fokotsa_ntsifatso_Boleng();
        if (처리값 < 0) { 명령해석기.phoso(처리값); return; }
        int 원본번호 = memori_Difaele.batla_tsenyo(); if (원본번호 < 0) { 명령해석기.phoso(-2); return; }
        int 항목수 = memori_Difaele.boleele_Boleng[원본번호]; for (int lupu_tshupane = 0; lupu_tshupane < 항목수; lupu_tshupane++) tshedimosetso[lupu_tshupane] = memori_Difaele.자료읽기(원본번호, lupu_tshupane);
        처리값 = 명령해석기.tsela(2); if (처리값 >= 0) 처리값 = memori_Difaele.fokotsa_ntsifatso_Boleng();
        if (처리값 < 0) { 명령해석기.phoso(처리값); return; }
        if (memori_Difaele.batla_tsenyo() == 원본번호) { if (!이동여부) 명령해석기.phoso(-22); return; }
        if (이동여부) { 처리값 = memori_Difaele.이름바꾸기(원본번호); if (처리값 < 0) 명령해석기.phoso(처리값); return; }
        int 열린파일번호 = memori_Difaele.bula(577); if (열린파일번호 < 0) { 명령해석기.phoso(열린파일번호); return; }
        for (int lupu_tshupane = 0; lupu_tshupane < 항목수; lupu_tshupane++) { 처리값 = memori_Difaele.kwala(열린파일번호, tshedimosetso[lupu_tshupane]); if (처리값 < 0) { 명령해석기.phoso(처리값); break; } }
        memori_Difaele.tswala(열린파일번호);
    }
    static int dijite_Boleng(int Thulaganyo_tshupane) {
        if (Thulaganyo_tshupane >= 명령해석기.토큰수) return -1;
        int 항목수 = 0; for (int lupu_tshupane = 0; lupu_tshupane < 명령해석기.boleele_Boleng[Thulaganyo_tshupane]; lupu_tshupane++) { int khoutuletshwao = 명령해석기.papetlana_Boleng[명령해석기.시작점[Thulaganyo_tshupane] + lupu_tshupane]; if (khoutuletshwao < '0' || khoutuletshwao > '9' || 항목수 > 10000) return -1; 항목수 = 항목수 * 10 + khoutuletshwao - '0'; } return 항목수;
    }
    static void 세기() {
        int Thulaganyo_tshupane = 1, 선택번호 = 0;
        if (명령해석기.같음(1, "-c") || 명령해석기.같음(1, "-l") || 명령해석기.같음(1, "-w")) { 선택번호 = 명령해석기.같음(1, "-c") ? 1 : 명령해석기.같음(1, "-l") ? 2 : 3; Thulaganyo_tshupane++; }
        if (명령해석기.토큰수 > Thulaganyo_tshupane + 1) { 명령해석기.결과 = 2; 단말.kwala("사용법: wc [-c|-l|-w] [faele]\n"); return; }
        if (!입력준비(Thulaganyo_tshupane)) return;
        int 바이트수 = 0, 줄수 = 0, 낱말수 = 0, baete_tshedimosetso; boolean 낱말 = false;
        while ((baete_tshedimosetso = 읽기()) >= 0 && baete_tshedimosetso != 256) { 바이트수++; if (baete_tshedimosetso == 10) 줄수++; boolean sebaka = baete_tshedimosetso == 32 || baete_tshedimosetso >= 9 && baete_tshedimosetso <= 13; if (!sebaka && !낱말) 낱말수++; 낱말 = !sebaka; }
        tswala(); if (baete_tshedimosetso < 0) { 명령해석기.phoso(baete_tshedimosetso); return; }
        if (선택번호 != 0) 단말.수(선택번호 == 1 ? 바이트수 : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.수(줄수); 단말.문자(' '); 단말.수(낱말수); 단말.문자(' '); 단말.수(바이트수); } 단말.문자(10);
    }
    static void batla_tsenyo() {
        if (명령해석기.토큰수 < 2 || 명령해석기.토큰수 > 3) { 명령해석기.결과 = 2; 단말.kwala("사용법: grep 찾을문구 [faele]\n"); return; }
        if (!입력준비(2)) return;
        int 항목수 = 0, baete_tshedimosetso, 일치수 = 0;
        while (true) {
            baete_tshedimosetso = 읽기();
            if (baete_tshedimosetso == 10 || baete_tshedimosetso == 256 || baete_tshedimosetso < 0) {
                boolean 찾은여부 = false;
                for (int lupu_tshupane = 0; lupu_tshupane <= 항목수 - 명령해석기.boleele_Boleng[1]; lupu_tshupane++) {
                    boolean 같은여부 = true; for (int 안쪽자리 = 0; 안쪽자리 < 명령해석기.boleele_Boleng[1]; 안쪽자리++) if (tshedimosetso[lupu_tshupane + 안쪽자리] != 명령해석기.papetlana_Boleng[명령해석기.시작점[1] + 안쪽자리]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (항목수 > 0 || baete_tshedimosetso == 10)) { for (int lupu_tshupane = 0; lupu_tshupane < 항목수; lupu_tshupane++) 보드.직렬쓰기(tshedimosetso[lupu_tshupane]); 단말.문자(10); 일치수++; }
                항목수 = 0; if (baete_tshedimosetso != 10) break;
            } else if (항목수 < tshedimosetso.length) tshedimosetso[항목수++] = baete_tshedimosetso;
            else { 명령해석기.phoso(-28); tswala(); return; }
        }
        tswala(); if (baete_tshedimosetso < 0) 명령해석기.phoso(baete_tshedimosetso); else if (명령해석기.결과 == 0) 명령해석기.결과 = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int Thulaganyo_tshupane = 1, 줄수 = 10;
        if (명령해석기.같음(1, "-n")) { 줄수 = dijite_Boleng(2); Thulaganyo_tshupane = 3; }
        if (줄수 < 0 || 명령해석기.토큰수 > Thulaganyo_tshupane + 1) { 명령해석기.결과 = 2; 단말.kwala("사용법: head/tail [-n 줄수] [faele]\n"); return; }
        if (!입력준비(Thulaganyo_tshupane)) return;
        int 항목수 = 0, baete_tshedimosetso;
        while ((baete_tshedimosetso = 읽기()) != 256 && baete_tshedimosetso >= 0) { if (항목수 == tshedimosetso.length) { 명령해석기.phoso(-28); tswala(); return; } tshedimosetso[항목수++] = baete_tshedimosetso; }
        tswala(); if (baete_tshedimosetso < 0) { 명령해석기.phoso(baete_tshedimosetso); return; }
        int e_e_gaufi_simolola = 0, 끝자리 = 항목수;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int 총수 = 0; for (int lupu_tshupane = 항목수 - 2; lupu_tshupane >= 0; lupu_tshupane--) if (tshedimosetso[lupu_tshupane] == 10 && ++총수 == 줄수) { e_e_gaufi_simolola = lupu_tshupane + 1; break; } }
        else { int 총수 = 0; for (int lupu_tshupane = 0; lupu_tshupane < 항목수; lupu_tshupane++) if (tshedimosetso[lupu_tshupane] == 10 && ++총수 == 줄수) { 끝자리 = lupu_tshupane + 1; break; } }
        for (int lupu_tshupane = e_e_gaufi_simolola; lupu_tshupane < 끝자리; lupu_tshupane++) 보드.직렬쓰기(tshedimosetso[lupu_tshupane]);
    }
    static void 함께쓰기() {
        boolean 덧붙임여부 = 명령해석기.같음(1, "-a"); int Thulaganyo_tshupane = 덧붙임여부 ? 2 : 1;
        if (명령해석기.토큰수 != Thulaganyo_tshupane + 1) { 명령해석기.결과 = 2; 단말.kwala("사용법: tee [-a] faele\n"); return; }
        int 열린파일번호 = bula_faele(Thulaganyo_tshupane, 덧붙임여부 ? 1089 : 577); if (열린파일번호 < 0) { 명령해석기.phoso(열린파일번호); return; }
        입력파일 = -1; int baete_tshedimosetso;
        while ((baete_tshedimosetso = 읽기()) != 256 && baete_tshedimosetso >= 0) { int 처리값 = memori_Difaele.kwala(열린파일번호, baete_tshedimosetso); if (처리값 < 0) { 명령해석기.phoso(처리값); break; } 보드.직렬쓰기(baete_tshedimosetso); }
        memori_Difaele.tswala(열린파일번호);
    }
}
