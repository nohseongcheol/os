// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 isihumushi_miyalelo 내장 Amathuluzi. */
public final class isihumushi_miyalelo_Amathuluzi {
    static int[] imininingwane = new int[16384];
    static int 입력파일 = -1;
    static int vula_ifayela(int i_agumenti_thola_inkomba, int Inqubo_inqubo) {
        int 처리값 = 명령해석기.Indlela_2(i_agumenti_thola_inkomba); return 처리값 < 0 ? 처리값 : inkumbulo_Amafayela.Vula(Inqubo_inqubo);
    }
    static boolean 입력준비(int i_agumenti_thola_inkomba) {
        입력파일 = -1;
        if (i_agumenti_thola_inkomba < 명령해석기.토큰수) {
            입력파일 = vula_ifayela(i_agumenti_thola_inkomba, 0);
            if (입력파일 < 0) { 명령해석기.Iphutha(입력파일); return false; }
        }
        return true;
    }
    static int Funda() {
        if (입력파일 >= 3) return inkumbulo_Amafayela.Funda(입력파일);
        while (true) {
            int ibhayithi_imininingwane = 보드.직렬읽기(); if (ibhayithi_imininingwane == -2 || ibhayithi_imininingwane == 4) return 256;
            if (ibhayithi_imininingwane == 3) { 명령해석기.결과 = 130; return 256; }
            if (ibhayithi_imininingwane >= 0) return ibhayithi_imininingwane; 보드.misa_okwesikhashana_i_CPU();
        }
    }
    static void Vala() { if (입력파일 >= 3) inkumbulo_Amafayela.Vala(입력파일); 입력파일 = -1; }
    static void buka_inani() {
        int 마지막자리 = 명령해석기.토큰수 == 1 ? 2 : 명령해석기.토큰수;
        for (int i_agumenti_thola_inkomba = 1; i_agumenti_thola_inkomba < 마지막자리; i_agumenti_thola_inkomba++) {
            if (!입력준비(i_agumenti_thola_inkomba)) continue;
            int ibhayithi_imininingwane; while ((ibhayithi_imininingwane = Funda()) != 256 && ibhayithi_imininingwane >= 0) 보드.직렬쓰기(ibhayithi_imininingwane);
            if (ibhayithi_imininingwane < 0) 명령해석기.Iphutha(ibhayithi_imininingwane); Vala();
        }
    }
    static void ifayela_udaba(String 동작번호) {
        if (명령해석기.토큰수 != 2) { 명령해석기.결과 = 2; 단말.Bhala("사용법: mkdir/rmdir/touch Ihele\n"); return; }
        int 처리값 = 명령해석기.Indlela_2(1);
        if (처리값 >= 0) {
            if (동작번호.charAt(0) == 'm') 처리값 = inkumbulo_Amafayela.yakha_umkhombandlela();
            else if (동작번호.charAt(0) == 'r') 처리값 = inkumbulo_Amafayela.khipha_umkhombandlela();
            else { 처리값 = inkumbulo_Amafayela.Vula(65); if (처리값 >= 3) 처리값 = inkumbulo_Amafayela.Vala(처리값); }
        }
        if (처리값 < 0) 명령해석기.Iphutha(처리값);
    }
    static void kopisha_inani(boolean 이동여부) {
        if (명령해석기.토큰수 != 3) { 명령해석기.결과 = 2; 단말.Bhala("사용법: cp/mv 원본 목적지 (Ihele)\n"); return; }
        int 처리값 = 명령해석기.Indlela_2(1); if (처리값 >= 0) 처리값 = inkumbulo_Amafayela.beka_kujwayeleke_inani();
        if (처리값 < 0) { 명령해석기.Iphutha(처리값); return; }
        int 원본번호 = inkumbulo_Amafayela.thola_okufakwayo(); if (원본번호 < 0) { 명령해석기.Iphutha(-2); return; }
        int 항목수 = inkumbulo_Amafayela.ubude_inani[원본번호]; for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 항목수; iluphu_thola_inkomba++) imininingwane[iluphu_thola_inkomba] = inkumbulo_Amafayela.자료읽기(원본번호, iluphu_thola_inkomba);
        처리값 = 명령해석기.Indlela_2(2); if (처리값 >= 0) 처리값 = inkumbulo_Amafayela.beka_kujwayeleke_inani();
        if (처리값 < 0) { 명령해석기.Iphutha(처리값); return; }
        if (inkumbulo_Amafayela.thola_okufakwayo() == 원본번호) { if (!이동여부) 명령해석기.Iphutha(-22); return; }
        if (이동여부) { 처리값 = inkumbulo_Amafayela.이름바꾸기(원본번호); if (처리값 < 0) 명령해석기.Iphutha(처리값); return; }
        int 열린파일번호 = inkumbulo_Amafayela.Vula(577); if (열린파일번호 < 0) { 명령해석기.Iphutha(열린파일번호); return; }
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 항목수; iluphu_thola_inkomba++) { 처리값 = inkumbulo_Amafayela.Bhala(열린파일번호, imininingwane[iluphu_thola_inkomba]); if (처리값 < 0) { 명령해석기.Iphutha(처리값); break; } }
        inkumbulo_Amafayela.Vala(열린파일번호);
    }
    static int idijithi_inani(int i_agumenti_thola_inkomba) {
        if (i_agumenti_thola_inkomba >= 명령해석기.토큰수) return -1;
        int 항목수 = 0; for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 명령해석기.ubude_inani[i_agumenti_thola_inkomba]; iluphu_thola_inkomba++) { int ikhodi_yohlamvu = 명령해석기.ithokhini_inani[명령해석기.시작점[i_agumenti_thola_inkomba] + iluphu_thola_inkomba]; if (ikhodi_yohlamvu < '0' || ikhodi_yohlamvu > '9' || 항목수 > 10000) return -1; 항목수 = 항목수 * 10 + ikhodi_yohlamvu - '0'; } return 항목수;
    }
    static void 세기() {
        int i_agumenti_thola_inkomba = 1, 선택번호 = 0;
        if (명령해석기.같음(1, "-c") || 명령해석기.같음(1, "-l") || 명령해석기.같음(1, "-w")) { 선택번호 = 명령해석기.같음(1, "-c") ? 1 : 명령해석기.같음(1, "-l") ? 2 : 3; i_agumenti_thola_inkomba++; }
        if (명령해석기.토큰수 > i_agumenti_thola_inkomba + 1) { 명령해석기.결과 = 2; 단말.Bhala("사용법: wc [-c|-l|-w] [Ihele]\n"); return; }
        if (!입력준비(i_agumenti_thola_inkomba)) return;
        int 바이트수 = 0, 줄수 = 0, 낱말수 = 0, ibhayithi_imininingwane; boolean 낱말 = false;
        while ((ibhayithi_imininingwane = Funda()) >= 0 && ibhayithi_imininingwane != 256) { 바이트수++; if (ibhayithi_imininingwane == 10) 줄수++; boolean indawo = ibhayithi_imininingwane == 32 || ibhayithi_imininingwane >= 9 && ibhayithi_imininingwane <= 13; if (!indawo && !낱말) 낱말수++; 낱말 = !indawo; }
        Vala(); if (ibhayithi_imininingwane < 0) { 명령해석기.Iphutha(ibhayithi_imininingwane); return; }
        if (선택번호 != 0) 단말.수(선택번호 == 1 ? 바이트수 : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.수(줄수); 단말.문자(' '); 단말.수(낱말수); 단말.문자(' '); 단말.수(바이트수); } 단말.문자(10);
    }
    static void thola_okufakwayo() {
        if (명령해석기.토큰수 < 2 || 명령해석기.토큰수 > 3) { 명령해석기.결과 = 2; 단말.Bhala("사용법: grep 찾을문구 [Ihele]\n"); return; }
        if (!입력준비(2)) return;
        int 항목수 = 0, ibhayithi_imininingwane, 일치수 = 0;
        while (true) {
            ibhayithi_imininingwane = Funda();
            if (ibhayithi_imininingwane == 10 || ibhayithi_imininingwane == 256 || ibhayithi_imininingwane < 0) {
                boolean 찾은여부 = false;
                for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba <= 항목수 - 명령해석기.ubude_inani[1]; iluphu_thola_inkomba++) {
                    boolean 같은여부 = true; for (int 안쪽자리 = 0; 안쪽자리 < 명령해석기.ubude_inani[1]; 안쪽자리++) if (imininingwane[iluphu_thola_inkomba + 안쪽자리] != 명령해석기.ithokhini_inani[명령해석기.시작점[1] + 안쪽자리]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (항목수 > 0 || ibhayithi_imininingwane == 10)) { for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 항목수; iluphu_thola_inkomba++) 보드.직렬쓰기(imininingwane[iluphu_thola_inkomba]); 단말.문자(10); 일치수++; }
                항목수 = 0; if (ibhayithi_imininingwane != 10) break;
            } else if (항목수 < imininingwane.length) imininingwane[항목수++] = ibhayithi_imininingwane;
            else { 명령해석기.Iphutha(-28); Vala(); return; }
        }
        Vala(); if (ibhayithi_imininingwane < 0) 명령해석기.Iphutha(ibhayithi_imininingwane); else if (명령해석기.결과 == 0) 명령해석기.결과 = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int i_agumenti_thola_inkomba = 1, 줄수 = 10;
        if (명령해석기.같음(1, "-n")) { 줄수 = idijithi_inani(2); i_agumenti_thola_inkomba = 3; }
        if (줄수 < 0 || 명령해석기.토큰수 > i_agumenti_thola_inkomba + 1) { 명령해석기.결과 = 2; 단말.Bhala("사용법: head/tail [-n 줄수] [Ihele]\n"); return; }
        if (!입력준비(i_agumenti_thola_inkomba)) return;
        int 항목수 = 0, ibhayithi_imininingwane;
        while ((ibhayithi_imininingwane = Funda()) != 256 && ibhayithi_imininingwane >= 0) { if (항목수 == imininingwane.length) { 명령해석기.Iphutha(-28); Vala(); return; } imininingwane[항목수++] = ibhayithi_imininingwane; }
        Vala(); if (ibhayithi_imininingwane < 0) { 명령해석기.Iphutha(ibhayithi_imininingwane); return; }
        int endaweni_qala = 0, 끝자리 = 항목수;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int 총수 = 0; for (int iluphu_thola_inkomba = 항목수 - 2; iluphu_thola_inkomba >= 0; iluphu_thola_inkomba--) if (imininingwane[iluphu_thola_inkomba] == 10 && ++총수 == 줄수) { endaweni_qala = iluphu_thola_inkomba + 1; break; } }
        else { int 총수 = 0; for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 항목수; iluphu_thola_inkomba++) if (imininingwane[iluphu_thola_inkomba] == 10 && ++총수 == 줄수) { 끝자리 = iluphu_thola_inkomba + 1; break; } }
        for (int iluphu_thola_inkomba = endaweni_qala; iluphu_thola_inkomba < 끝자리; iluphu_thola_inkomba++) 보드.직렬쓰기(imininingwane[iluphu_thola_inkomba]);
    }
    static void 함께쓰기() {
        boolean 덧붙임여부 = 명령해석기.같음(1, "-a"); int i_agumenti_thola_inkomba = 덧붙임여부 ? 2 : 1;
        if (명령해석기.토큰수 != i_agumenti_thola_inkomba + 1) { 명령해석기.결과 = 2; 단말.Bhala("사용법: tee [-a] Ihele\n"); return; }
        int 열린파일번호 = vula_ifayela(i_agumenti_thola_inkomba, 덧붙임여부 ? 1089 : 577); if (열린파일번호 < 0) { 명령해석기.Iphutha(열린파일번호); return; }
        입력파일 = -1; int ibhayithi_imininingwane;
        while ((ibhayithi_imininingwane = Funda()) != 256 && ibhayithi_imininingwane >= 0) { int 처리값 = inkumbulo_Amafayela.Bhala(열린파일번호, ibhayithi_imininingwane); if (처리값 < 0) { 명령해석기.Iphutha(처리값); break; } 보드.직렬쓰기(ibhayithi_imininingwane); }
        inkumbulo_Amafayela.Vala(열린파일번호);
    }
}
