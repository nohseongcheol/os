// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 blaosc 내장 Uirlisí. */
public final class blaosc_Uirlisí {
    static int[] sonraí = new int[16384];
    static int 입력파일 = -1;
    static int oscail_comhad(int argóint_INDEX, int Próiseas_mód) {
        int 처리값 = 명령해석기.CONAIR(argóint_INDEX); return 처리값 < 0 ? 처리값 : Cuimhne_Comhaid.Oscail(Próiseas_mód);
    }
    static boolean 입력준비(int argóint_INDEX) {
        입력파일 = -1;
        if (argóint_INDEX < 명령해석기.licín_COUNT) {
            입력파일 = oscail_comhad(argóint_INDEX, 0);
            if (입력파일 < 0) { 명령해석기.ERREÁID(입력파일); return false; }
        }
        return true;
    }
    static int Léigh() {
        if (입력파일 >= 3) return Cuimhne_Comhaid.Léigh(입력파일);
        while (true) {
            int beart_sonraí = clár.직렬읽기(); if (beart_sonraí == -2 || beart_sonraí == 4) return 256;
            if (beart_sonraí == 3) { 명령해석기.tomhas = 130; return 256; }
            if (beart_sonraí >= 0) return beart_sonraí; clár.YIELD_CPU();
        }
    }
    static void Dún() { if (입력파일 >= 3) Cuimhne_Comhaid.Dún(입력파일); 입력파일 = -1; }
    static void Amharc_VALUE() {
        int 마지막자리 = 명령해석기.licín_COUNT == 1 ? 2 : 명령해석기.licín_COUNT;
        for (int argóint_INDEX = 1; argóint_INDEX < 마지막자리; argóint_INDEX++) {
            if (!입력준비(argóint_INDEX)) continue;
            int beart_sonraí; while ((beart_sonraí = Léigh()) != 256 && beart_sonraí >= 0) clár.직렬쓰기(beart_sonraí);
            if (beart_sonraí < 0) 명령해석기.ERREÁID(beart_sonraí); Dún();
        }
    }
    static void comhad_cás(String 동작번호) {
        if (명령해석기.licín_COUNT != 2) { 명령해석기.tomhas = 2; 단말.Scríobh("사용법: mkdir/rmdir/touch Comhad\n"); return; }
        int 처리값 = 명령해석기.CONAIR(1);
        if (처리값 >= 0) {
            if (동작번호.charAt(0) == 'm') 처리값 = Cuimhne_Comhaid.Create_eolaire();
            else if (동작번호.charAt(0) == 'r') 처리값 = Cuimhne_Comhaid.bain_eolaire();
            else { 처리값 = Cuimhne_Comhaid.Oscail(65); if (처리값 >= 3) 처리값 = Cuimhne_Comhaid.Dún(처리값); }
        }
        if (처리값 < 0) 명령해석기.ERREÁID(처리값);
    }
    static void ásc_VALUE(boolean 이동여부) {
        if (명령해석기.licín_COUNT != 3) { 명령해석기.tomhas = 2; 단말.Scríobh("사용법: cp/mv 원본 목적지 (Comhad)\n"); return; }
        int 처리값 = 명령해석기.CONAIR(1); if (처리값 >= 0) 처리값 = Cuimhne_Comhaid.normalaigh_VALUE();
        if (처리값 < 0) { 명령해석기.ERREÁID(처리값); return; }
        int 원본번호 = Cuimhne_Comhaid.FIND_iontráil(); if (원본번호 < 0) { 명령해석기.ERREÁID(-2); return; }
        int iontráil_COUNT = Cuimhne_Comhaid.fad_VALUE[원본번호]; for (int lúb_INDEX = 0; lúb_INDEX < iontráil_COUNT; lúb_INDEX++) sonraí[lúb_INDEX] = Cuimhne_Comhaid.자료읽기(원본번호, lúb_INDEX);
        처리값 = 명령해석기.CONAIR(2); if (처리값 >= 0) 처리값 = Cuimhne_Comhaid.normalaigh_VALUE();
        if (처리값 < 0) { 명령해석기.ERREÁID(처리값); return; }
        if (Cuimhne_Comhaid.FIND_iontráil() == 원본번호) { if (!이동여부) 명령해석기.ERREÁID(-22); return; }
        if (이동여부) { 처리값 = Cuimhne_Comhaid.이름바꾸기(원본번호); if (처리값 < 0) 명령해석기.ERREÁID(처리값); return; }
        int 열린파일번호 = Cuimhne_Comhaid.Oscail(577); if (열린파일번호 < 0) { 명령해석기.ERREÁID(열린파일번호); return; }
        for (int lúb_INDEX = 0; lúb_INDEX < iontráil_COUNT; lúb_INDEX++) { 처리값 = Cuimhne_Comhaid.Scríobh(열린파일번호, sonraí[lúb_INDEX]); if (처리값 < 0) { 명령해석기.ERREÁID(처리값); break; } }
        Cuimhne_Comhaid.Dún(열린파일번호);
    }
    static int digit_VALUE(int argóint_INDEX) {
        if (argóint_INDEX >= 명령해석기.licín_COUNT) return -1;
        int iontráil_COUNT = 0; for (int lúb_INDEX = 0; lúb_INDEX < 명령해석기.fad_VALUE[argóint_INDEX]; lúb_INDEX++) { int pointe_cóid = 명령해석기.licín_VALUE[명령해석기.시작점[argóint_INDEX] + lúb_INDEX]; if (pointe_cóid < '0' || pointe_cóid > '9' || iontráil_COUNT > 10000) return -1; iontráil_COUNT = iontráil_COUNT * 10 + pointe_cóid - '0'; } return iontráil_COUNT;
    }
    static void 세기() {
        int argóint_INDEX = 1, 선택번호 = 0;
        if (명령해석기.같음(1, "-c") || 명령해석기.같음(1, "-l") || 명령해석기.같음(1, "-w")) { 선택번호 = 명령해석기.같음(1, "-c") ? 1 : 명령해석기.같음(1, "-l") ? 2 : 3; argóint_INDEX++; }
        if (명령해석기.licín_COUNT > argóint_INDEX + 1) { 명령해석기.tomhas = 2; 단말.Scríobh("사용법: wc [-c|-l|-w] [Comhad]\n"); return; }
        if (!입력준비(argóint_INDEX)) return;
        int beart_COUNT = 0, 줄수 = 0, 낱말수 = 0, beart_sonraí; boolean 낱말 = false;
        while ((beart_sonraí = Léigh()) >= 0 && beart_sonraí != 256) { beart_COUNT++; if (beart_sonraí == 10) 줄수++; boolean spás = beart_sonraí == 32 || beart_sonraí >= 9 && beart_sonraí <= 13; if (!spás && !낱말) 낱말수++; 낱말 = !spás; }
        Dún(); if (beart_sonraí < 0) { 명령해석기.ERREÁID(beart_sonraí); return; }
        if (선택번호 != 0) 단말.수(선택번호 == 1 ? beart_COUNT : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.수(줄수); 단말.문자(' '); 단말.수(낱말수); 단말.문자(' '); 단말.수(beart_COUNT); } 단말.문자(10);
    }
    static void FIND_iontráil() {
        if (명령해석기.licín_COUNT < 2 || 명령해석기.licín_COUNT > 3) { 명령해석기.tomhas = 2; 단말.Scríobh("사용법: grep 찾을문구 [Comhad]\n"); return; }
        if (!입력준비(2)) return;
        int iontráil_COUNT = 0, beart_sonraí, 일치수 = 0;
        while (true) {
            beart_sonraí = Léigh();
            if (beart_sonraí == 10 || beart_sonraí == 256 || beart_sonraí < 0) {
                boolean 찾은여부 = false;
                for (int lúb_INDEX = 0; lúb_INDEX <= iontráil_COUNT - 명령해석기.fad_VALUE[1]; lúb_INDEX++) {
                    boolean 같은여부 = true; for (int comhcheangal_istigh_suíomh = 0; comhcheangal_istigh_suíomh < 명령해석기.fad_VALUE[1]; comhcheangal_istigh_suíomh++) if (sonraí[lúb_INDEX + comhcheangal_istigh_suíomh] != 명령해석기.licín_VALUE[명령해석기.시작점[1] + comhcheangal_istigh_suíomh]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (iontráil_COUNT > 0 || beart_sonraí == 10)) { for (int lúb_INDEX = 0; lúb_INDEX < iontráil_COUNT; lúb_INDEX++) clár.직렬쓰기(sonraí[lúb_INDEX]); 단말.문자(10); 일치수++; }
                iontráil_COUNT = 0; if (beart_sonraí != 10) break;
            } else if (iontráil_COUNT < sonraí.length) sonraí[iontráil_COUNT++] = beart_sonraí;
            else { 명령해석기.ERREÁID(-28); Dún(); return; }
        }
        Dún(); if (beart_sonraí < 0) 명령해석기.ERREÁID(beart_sonraí); else if (명령해석기.tomhas == 0) 명령해석기.tomhas = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int argóint_INDEX = 1, 줄수 = 10;
        if (명령해석기.같음(1, "-n")) { 줄수 = digit_VALUE(2); argóint_INDEX = 3; }
        if (줄수 < 0 || 명령해석기.licín_COUNT > argóint_INDEX + 1) { 명령해석기.tomhas = 2; 단말.Scríobh("사용법: head/tail [-n 줄수] [Comhad]\n"); return; }
        if (!입력준비(argóint_INDEX)) return;
        int iontráil_COUNT = 0, beart_sonraí;
        while ((beart_sonraí = Léigh()) != 256 && beart_sonraí >= 0) { if (iontráil_COUNT == sonraí.length) { 명령해석기.ERREÁID(-28); Dún(); return; } sonraí[iontráil_COUNT++] = beart_sonraí; }
        Dún(); if (beart_sonraí < 0) { 명령해석기.ERREÁID(beart_sonraí); return; }
        int logánta_Start = 0, cuir_deireadh_le_suíomh = iontráil_COUNT;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int 총수 = 0; for (int lúb_INDEX = iontráil_COUNT - 2; lúb_INDEX >= 0; lúb_INDEX--) if (sonraí[lúb_INDEX] == 10 && ++총수 == 줄수) { logánta_Start = lúb_INDEX + 1; break; } }
        else { int 총수 = 0; for (int lúb_INDEX = 0; lúb_INDEX < iontráil_COUNT; lúb_INDEX++) if (sonraí[lúb_INDEX] == 10 && ++총수 == 줄수) { cuir_deireadh_le_suíomh = lúb_INDEX + 1; break; } }
        for (int lúb_INDEX = logánta_Start; lúb_INDEX < cuir_deireadh_le_suíomh; lúb_INDEX++) clár.직렬쓰기(sonraí[lúb_INDEX]);
    }
    static void 함께쓰기() {
        boolean 덧붙임여부 = 명령해석기.같음(1, "-a"); int argóint_INDEX = 덧붙임여부 ? 2 : 1;
        if (명령해석기.licín_COUNT != argóint_INDEX + 1) { 명령해석기.tomhas = 2; 단말.Scríobh("사용법: tee [-a] Comhad\n"); return; }
        int 열린파일번호 = oscail_comhad(argóint_INDEX, 덧붙임여부 ? 1089 : 577); if (열린파일번호 < 0) { 명령해석기.ERREÁID(열린파일번호); return; }
        입력파일 = -1; int beart_sonraí;
        while ((beart_sonraí = Léigh()) != 256 && beart_sonraí >= 0) { int 처리값 = Cuimhne_Comhaid.Scríobh(열린파일번호, beart_sonraí); if (처리값 < 0) { 명령해석기.ERREÁID(처리값); break; } clár.직렬쓰기(beart_sonraí); }
        Cuimhne_Comhaid.Dún(열린파일번호);
    }
}
